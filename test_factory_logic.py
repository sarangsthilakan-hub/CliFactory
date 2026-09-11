import pytest
from unittest.mock import patch
from factory_logic import (
    create_initial_game_state,
    is_bankrupt,
    has_achieved_monopoly,
    get_current_factory_title,
    calculate_effective_risk,
    execute_factory_expansion,
    execute_rd_investment,
    execute_sales_contract,
    process_end_of_month_rollover,
    evaluate_minor_action_risk
)


@pytest.fixture
def base_state():
    """Provides a fresh game state for each test to prevent mutation leakage."""
    return create_initial_game_state("Mid-Market", 500.0, 2)


# --- BVA: Bankruptcy Limits ---
def test_is_bankrupt_bva(base_state):
    base_state["capital"] = 0.01
    assert not is_bankrupt(base_state)  # Just above boundary
    base_state["capital"] = 0.0
    assert is_bankrupt(base_state)  # Exact boundary
    base_state["capital"] = -0.01
    assert is_bankrupt(base_state)  # Just below boundary


# --- EP & BVA: Monopoly Conditions ---
def test_monopoly_easy_bva():
    state = create_initial_game_state("Subsidized Startup", 5000.0, 4)
    # Tier 3 output: 18 + (3 * 15) = 63 (Passes the >= 50 requirement)
    state["factory_expansion_tier"] = 3

    assert has_achieved_monopoly(state)

    # Boundary: Capital just 1 cent below the 5000 threshold
    state["capital"] = 4999.99
    assert not has_achieved_monopoly(state)


# --- BVA: Risk Clamping ---
def test_effective_risk_clamping(base_state):
    # Test lower bound clamping (should not drop below 0.05)
    base_state["negative_event_chance"] = 0.0
    assert calculate_effective_risk(base_state) == 0.05

    # Test upper bound clamping (should not exceed 1.0)
    base_state["negative_event_chance"] = 1.5
    assert calculate_effective_risk(base_state) == 1.0


# --- EP: Factory Expansion Strategies ---
@pytest.mark.parametrize("strategy, expected_upkeep, expected_risk", [
    ("1", 65, 0.31),  # EP 1: Ruthless (+15 upkeep, +0.06 risk)
    ("2", 75, 0.13),  # EP 2: Safety (+25 upkeep, -0.12 risk)
    ("3", 55, 0.40),  # EP 3: Cost-cut (+5 upkeep, +0.15 risk)
    ("4", 70, 0.25),  # EP 4: Default (+20 upkeep, no risk change)
])
def test_factory_expansion_strategies_ep(base_state, strategy, expected_upkeep, expected_risk):
    new_state = execute_factory_expansion(base_state, strategy)
    assert new_state["base_maintenance_cost"] == expected_upkeep
    assert round(new_state["negative_event_chance"], 2) == expected_risk


# --- BVA: Sales Constraints ---
def test_sales_contract_bva(base_state):
    base_state["finished_goods"] = 60
    base_state["max_sell_limit"] = 50

    # Requesting to sell 60, but max limit is 50. System must clamp to 50.
    new_state, earned, sold = execute_sales_contract(base_state, 60)
    assert sold == 50
    assert new_state["finished_goods"] == 10  # 60 total - 50 sold


# --- EP & BVA: Month Rollover & Futures Quota ---
def test_rollover_futures_contract_bva(base_state):
    base_state["futures_contract_active"] = True
    base_state["futures_quota_target"] = 40
    base_state["capital"] = 1000.0

    # BVA Fail: Exactly 1 unit short of quota (39). Expect 10% penalty on 1000.
    fail_state = base_state.copy()
    fail_state["total_goods_sold_this_month"] = 39
    new_fail_state, _ = process_end_of_month_rollover(fail_state, False)
    assert new_fail_state["capital"] == 900.0 - new_fail_state["base_maintenance_cost"]

    # BVA Success: Exact quota met (40). No penalty, contract fulfilled.
    success_state = base_state.copy()
    success_state["total_goods_sold_this_month"] = 40
    new_success_state, _ = process_end_of_month_rollover(success_state, False)
    assert new_success_state["capital"] == 1000.0 - new_success_state["base_maintenance_cost"]
    assert new_success_state["futures_contracts_fulfilled"] == 1


# --- EP: RNG Event Mocking ---
@patch("random.random")
def test_evaluate_minor_action_risk(mock_random, base_state):
    # Setup effective risk to be 0.25
    mock_random.return_value = 0.20  # Roll below risk (Triggers hazard)
    assert evaluate_minor_action_risk(base_state) is True

    mock_random.return_value = 0.30  # Roll above risk (Safe)
    assert evaluate_minor_action_risk(base_state) is False