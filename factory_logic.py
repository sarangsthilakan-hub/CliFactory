import random


def create_initial_game_state(difficulty_name, starting_capital, guaranteed_months):
    return {
        "difficulty_name": difficulty_name,
        "capital": starting_capital,
        "guaranteed_months": guaranteed_months,
        "current_month": 1,

        # Inventories
        "raw_materials": 20,
        "finished_goods": 0,

        # Factory Parameters
        "factory_expansion_tier": 0,
        "factory_tier_names": [
            "Factory",
            "Large Factory",
            "Large Factory Complex",
            "Mega Factory",
            "Mega Factory Supercomplex",
            "Ultra-Industrial Zenith Complex",
        ],
        "base_maintenance_cost": 50,
        "expansion_cost": 300,
        "max_sell_limit": 50,

        # Contracts & Modifiers
        "futures_contract_active": False,
        "futures_quota_target": 40,
        "market_price_multiplier": 20.0,

        # Turn Constraints & Special Flags
        "major_action_taken": False,
        "max_minor_actions": 2,
        "minor_actions_used": 0,
        "skip_next_major": False,
        "operations_locked_turns": 0,
        "next_major_yield_bonus": 0.0,

        # Research & Risk
        "research_levels": {
            "logistics": 0,
            "efficiency": 0,
            "safety": 0,
            "marketing": 0,
        },
        "negative_event_chance": 0.25,
        "total_goods_sold_this_month": 0,
    }


def is_bankrupt(game_state):
    return game_state["capital"] <= 0


def has_achieved_monopoly(game_state):
    total_output_rate = 18 + (game_state["factory_expansion_tier"] * 15)
    return game_state["capital"] >= 10000.0 and total_output_rate >= 100


def get_current_factory_title(game_state):
    tiers = game_state["factory_tier_names"]
    tier_index = min(game_state["factory_expansion_tier"], len(tiers) - 1)
    return tiers[tier_index]


def execute_factory_expansion(game_state, strategy_type):
    state = game_state.copy()
    state["capital"] -= state["expansion_cost"]
    state["factory_expansion_tier"] += 1
    state["major_action_taken"] = True

    if strategy_type == "1":  # Ruthless Efficiency
        state["base_maintenance_cost"] += 15
        state["negative_event_chance"] += 0.06
    elif strategy_type == "2":  # Safety-First Focus
        state["base_maintenance_cost"] += 25
        state["negative_event_chance"] = max(0.01, state["negative_event_chance"] - 0.12)
    elif strategy_type == "3":  # Cost-Cutting Focus
        state["base_maintenance_cost"] += 5
        state["negative_event_chance"] += 0.15
    else:  # Balanced Default
        state["base_maintenance_cost"] += 20

    return state


def execute_rd_investment(game_state, selected_field):
    state = game_state.copy()
    state["capital"] -= 100
    state["major_action_taken"] = True

    state["research_levels"][selected_field] += 1
    tier = state["research_levels"][selected_field]

    if selected_field == "logistics":
        if tier == 1:
            state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] - 5)
        elif tier == 2:
            state["max_sell_limit"] += 20
            state["base_maintenance_cost"] += 10
        elif tier == 3:
            state["max_sell_limit"] += 50
            state["base_maintenance_cost"] += 5
        elif tier == 4:
            state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] - 15)

    elif selected_field == "efficiency":
        if tier == 1:
            state["base_maintenance_cost"] += 5
        elif tier == 2:
            state["base_maintenance_cost"] -= 5
            state["expansion_cost"] += 20

    elif selected_field == "safety":
        state["base_maintenance_cost"] += (2 + tier)

    return state


def execute_sales_contract(game_state, quantity_to_sell):
    state = game_state.copy()

    unit_price = state["market_price_multiplier"]
    if state["research_levels"]["logistics"] >= 2:
        unit_price *= 1.20
    if state["research_levels"]["logistics"] >= 3:
        unit_price *= 1.10

    if state["futures_contract_active"]:
        unit_price *= 2.5
        state["futures_contract_active"] = False

    sold_amount = min(quantity_to_sell, state["max_sell_limit"], state["finished_goods"])
    earned_revenue = sold_amount * unit_price

    state["finished_goods"] -= sold_amount
    state["capital"] += earned_revenue
    state["total_goods_sold_this_month"] += sold_amount

    return state, earned_revenue, sold_amount


def process_end_of_month_rollover(game_state, cave_in_occurred):
    state = game_state.copy()

    # Futures Contract Quota Check
    if state["futures_contract_active"]:
        if state["total_goods_sold_this_month"] < state["futures_quota_target"]:
            penalty = state["capital"] * 0.10
            state["capital"] -= penalty
        state["futures_contract_active"] = False

    # Marketing Quota Check
    marketing_tier = state["research_levels"]["marketing"]
    quota_targets = {1: 50, 2: 70, 3: 90, 4: 120}
    quota_bonuses = {1: 0.05, 2: 0.10, 3: 0.15, 4: 0.25}

    if marketing_tier > 0:
        target_qty = quota_targets[marketing_tier]
        if state["total_goods_sold_this_month"] >= target_qty:
            bonus_cash = state["capital"] * quota_bonuses[marketing_tier]
            state["capital"] += bonus_cash

    # Passive Mining & Refining
    eff_tier = state["research_levels"]["efficiency"]
    mining_bonus = 0
    refining_bonus = 0

    if eff_tier >= 3:
        mining_bonus += 20
        refining_bonus += 5
    if eff_tier >= 4:
        mining_bonus += 35

    total_mined = 25 + (state["factory_expansion_tier"] * 5) + mining_bonus

    if cave_in_occurred:
        state["capital"] -= 90
        total_mined = 0
    else:
        state["raw_materials"] += total_mined

    total_refining_capacity = 18 + (state["factory_expansion_tier"] * 15) + refining_bonus
    if eff_tier >= 1:
        total_refining_capacity += 5
    if eff_tier >= 2:
        total_refining_capacity += 10

    actual_refined = min(state["raw_materials"], total_refining_capacity)
    state["raw_materials"] -= actual_refined
    state["finished_goods"] += actual_refined

    # Maintenance Upkeep
    state["capital"] -= state["base_maintenance_cost"]

    # Rollover resets
    if state["operations_locked_turns"] > 0:
        state["operations_locked_turns"] -= 1

    state["current_month"] += 1
    state["major_action_taken"] = False
    state["skip_next_major"] = False
    state["minor_actions_used"] = 0
    state["total_goods_sold_this_month"] = 0
    state["next_major_yield_bonus"] = 0.0

    return state