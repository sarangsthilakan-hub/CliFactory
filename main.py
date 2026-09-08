import os
import random
from factory_logic import (
    create_initial_game_state,
    is_bankrupt,
    has_achieved_monopoly,
    get_current_factory_title,
    execute_factory_expansion,
    execute_rd_investment,
    execute_sales_contract,
    process_end_of_month_rollover,
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def select_difficulty():
    while True:
        clear_screen()
        print("=" * 75)
        print("          🏭 CLIFACTORY: SELECT CORPORATE TIER 🏭          ")
        print("=" * 75)
        print("   [1] SUBSIDIZED STARTUP (Easy)")
        print("       - Starting Capital: $800.00")
        print("       - Guaranteed Positive Outcomes: First 4 Months")
        print("\n   [2] MID-MARKET (Normal)")
        print("       - Starting Capital: $500.00")
        print("       - Guaranteed Positive Outcomes: First 2 Months")
        print("\n   [3] HOSTILE TAKEOVER (Hard)")
        print("       - Starting Capital: $250.00")
        print("       - Guaranteed Positive Outcomes: None (Pure RNG)")
        print("-" * 75)

        choice = input("Select tier (1-3): ").strip()

        if choice == "1":
            return "Subsidized Startup", 800.0, 4
        elif choice == "2":
            return "Mid-Market", 500.0, 2
        elif choice == "3":
            return "Hostile Takeover", 250.0, 0
        else:
            input("\n[!] Invalid choice. Press Enter to try again.")


def run_game():
    diff_name, starting_capital, guaranteed_months = select_difficulty()
    state = create_initial_game_state(diff_name, starting_capital, guaranteed_months)

    while True:
        # Check Loss Condition
        if is_bankrupt(state):
            clear_screen()
            print("=" * 75)
            print("                     💀 GAME OVER: BANKRUPTCY 💀                     ")
            print("=" * 75)
            print(f" Month Reached: {state['current_month']}")
            print(" Capital reserves have hit $0. Hostile corporate buyout executed.")
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        # Check Victory Condition
        if has_achieved_monopoly(state):
            clear_screen()
            print("=" * 75)
            print("                   👑 VICTORY: GLOBAL MONOPOLY 👑                    ")
            print("=" * 75)
            print(f" Month Reached: {state['current_month']}")
            print(f" Final Capital: ${state['capital']:.2f}")
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        clear_screen()

        # Render Dashboard Header & Status Panel
        factory_title = get_current_factory_title(state)
        header_left = f"🏭 CLIFACTORY [{state['difficulty_name'].upper()}]"
        header_right = f"📅 MONTH: {state['current_month']}"
        print("=" * 75)
        print(f"{header_left:<45}{header_right:>28}")
        print("=" * 75)

        print(f" Facility Scale: [{factory_title}] (Level {state['factory_expansion_tier']})")
        print(
            f" Capital: ${state['capital']:.2f}  |  Raw Materials: {state['raw_materials']}"
            f"  |  Finished Goods: {state['finished_goods']}"
        )
        print(
            f" Upkeep: ${state['base_maintenance_cost']}/mo  |  Max Sell Limit:"
            f" {state['max_sell_limit']} units/contract"
        )
        print(
            f" Tech Tiers -> Logistics: {state['research_levels']['logistics']}/4 |"
            f" Efficiency: {state['research_levels']['efficiency']}/4 | Safety:"
            f" {state['research_levels']['safety']}/4 | Marketing:"
            f" {state['research_levels']['marketing']}/4"
        )

        if state["current_month"] <= state["guaranteed_months"]:
            print(
                " Status: 🛡️ Guaranteed Positive Outcome Active"
                f" ({state['guaranteed_months'] - state['current_month'] + 1} months left)"
            )
        else:
            print(" Status: ⚠️ Standard Market Risk Active")

        if state["futures_contract_active"]:
            print(f" Status Alert: 📈 Futures Contract Active (Quota: {state['futures_quota_target']} goods)")

        if state["skip_next_major"]:
            print(" Status Alert: 🔴 Major Action locked due to prior failure!")

        print(
            f" Actions Left this Month -> Major: "
            f"{'0/1 (Done/Locked)' if (state['major_action_taken'] or state['skip_next_major']) else '1 Available'}"
            f" | Minor: {state['max_minor_actions'] - state['minor_actions_used']}/{state['max_minor_actions']}"
        )
        print("-" * 75)

        # Main Interface Menu
        print(" CHOOSE YOUR ACTIONS:")
        print("\n [MAJOR ACTIONS (Max 1 per month)]")
        if not state["major_action_taken"] and not state["skip_next_major"]:
            print("   [1] Prospect Unknown Sector (High risk / reward exploration pool)")
            print(f"   [2] Construct Factory Expansion (Structural upgrade: -${state['expansion_cost']} Cap)")
            print("   [3] Invest in R&D (Research Logistics, Efficiency, Safety, Marketing)")
            print(f"   [4] Corporate Futures Contract (Commit to selling {state['futures_quota_target']}+ goods)")
            print("   [5] Bulk Material Import (Emergency supply chain safety net: +150 Raw for $200)")
        else:
            print("   [1-5] (Major Action unavailable or completed this month)")

        print("\n [MINOR ACTIONS (Limited per month)]")
        print("   [6] Execute Tactical Minor Action (Operations, Maintenance, Market, Logistics, HR)")
        print("   [7] Secure Sales Contract & Sell Finished Goods on Market")

        print("\n [SYSTEM CONTROLS]")
        print("   [8] End Month Early & Proceed to Next Cycle")
        print("   [9] Quit Game")
        print("-" * 75)

        choice = input("Select an option (1-9): ").strip()

        # Handle Major Actions [1-5]
        if choice in ["1", "2", "3", "4", "5"]:
            if state["major_action_taken"] or state["skip_next_major"]:
                clear_screen()
                print("\n[!] Major Action is locked or already performed this month!")
                input("Press Enter to continue.")
                continue

            clear_screen()

            if choice == "1":
                state["major_action_taken"] = True
                print(f"--- MONTH {state['current_month']}: PROSPECT UNKNOWN SECTOR ---")

                if state["current_month"] <= state["guaranteed_months"]:
                    event_roll = random.choice(["high_yield", "geode", "shaft"])
                else:
                    hazard_chance = max(0.05,
                                        state["negative_event_chance"] - (state["research_levels"]["safety"] * 0.05))
                    roll_type = random.random()
                    if roll_type < hazard_chance:
                        event_roll = random.choice(["gas", "seepage", "slip", "insects"])
                    elif roll_type < hazard_chance + 0.35:
                        event_roll = random.choice(["high_yield", "unstable", "shaft", "geode"])
                    else:
                        event_roll = random.choice(["barren", "cavern"])

                if event_roll == "high_yield":
                    state["raw_materials"] += 75
                    print("\n [Success]: Located a rich rare mineral vein.\n Effect: +75 Raw Materials")
                elif event_roll == "unstable":
                    print("\n [Discovery]: Encountered Unstable Soil formations.")
                    sub = input("   Keep digging deeper [1] or Cease operations [2]? ").strip()
                    if sub == "1" and random.random() < 0.5:
                        state["raw_materials"] += 125
                        print("\n [Deep Dig Success]: +125 Raw Materials")
                    elif sub == "1":
                        state["capital"] -= 40
                        print("\n [Cave-in Hazard]: Minor equipment damage cost -$40.")
                    else:
                        print("\n [Safe Call]: Ceased operations safely.")
                elif event_roll == "geode":
                    state["capital"] += 300
                    print("\n [JACKPOT!]: Precious gemstone geode found! (+300 Capital)")
                elif event_roll == "shaft":
                    state["raw_materials"] += 90
                    print("\n [Salvage]: Abandoned mining cache found. (+90 Raw Materials)")
                elif event_roll in ["barren", "cavern"]:
                    print("\n [Dead End]: Finds nothing of importance.")
                elif event_roll == "gas":
                    state["capital"] -= 30
                    print("\n [Hazard]: Corrosive gas pocket. Filter replacements cost -$30.")
                elif event_roll == "seepage":
                    state["capital"] -= 40
                    print("\n [Hazard]: Water seepage. Pumping equipment cost -$40.")
                elif event_roll == "slip":
                    state["capital"] -= 45
                    print("\n [Hazard]: Rockshift misaligned gear. Alignment cost -$45.")
                elif event_roll == "insects":
                    state["capital"] -= 35
                    print("\n [Hazard]: Pests chewed wiring. Harness repairs cost -$35.")

            elif choice == "2":
                print(f"--- MONTH {state['current_month']}: CONSTRUCT FACTORY EXPANSION ---")
                if state["capital"] >= state["expansion_cost"]:
                    print(f"Expansion Cost: ${state['expansion_cost']}")
                    print("Select your factory expansion focus strategy:\n")
                    print("  [1] Ruthless Efficiency (+20 capacity, +$15 upkeep, +6% risk)")
                    print("  [2] Safety-First Focus (+10 capacity, +$25 upkeep, -12% risk)")
                    print("  [3] Cost-Cutting Focus (+15 capacity, +$5 upkeep, +15% risk)")

                    strat_choice = input("\nSelect strategy (1-3): ").strip()
                    state = execute_factory_expansion(state, strat_choice)
                    print("\n[Expansion Successful]: Factory successfully upgraded!")
                else:
                    print(f"\n[!] Insufficient Capital! Construction requires ${state['expansion_cost']}.")

            elif choice == "3":
                print(f"--- MONTH {state['current_month']}: RESEARCH & DEVELOPMENT ---")
                print("Select a research field to invest in (-$100 Funds):")
                print(f"  [1] Logistics [Tier: {state['research_levels']['logistics']}/4]")
                print(f"  [2] Efficiency [Tier: {state['research_levels']['efficiency']}/4]")
                print(f"  [3] Safety [Tier: {state['research_levels']['safety']}/4]")
                print(f"  [4] Marketing [Tier: {state['research_levels']['marketing']}/4]")
                print("  [5] Cancel R&D Investment")

                rd_choice = input("\nSelect field (1-5): ").strip()
                if rd_choice in ["1", "2", "3", "4"]:
                    field_map = {"1": "logistics", "2": "efficiency", "3": "safety", "4": "marketing"}
                    field = field_map[rd_choice]

                    if state["research_levels"][field] >= 4:
                        print("\n[!] All technologies for this field are fully researched!")
                    elif state["capital"] >= 100:
                        fail_chance = 0.0 if (state["current_month"] <= state[
                            "guaranteed_months"] or field == "marketing") else 0.05
                        if random.random() < fail_chance:
                            state["capital"] -= 100
                            state["major_action_taken"] = True
                            print("\n[!] RESEARCH FAILURE! -$100 funds wasted with no tech unlocked.")
                        else:
                            state = execute_rd_investment(state, field)
                            print(f"\n[Success]: Successfully advanced {field.capitalize()} R&D tier!")
                    else:
                        print("\n[!] Insufficient Capital! R&D requires $100.")

            elif choice == "4":
                state["major_action_taken"] = True
                state["futures_contract_active"] = True
                print(f"--- MONTH {state['current_month']}: CORPORATE FUTURES CONTRACT ---")
                print(
                    f"\nSecured futures contract! Target quota: {state['futures_quota_target']} goods for 2.5x price bonus.")

            elif choice == "5":
                print(f"--- MONTH {state['current_month']}: BULK MATERIAL IMPORT ---")
                if state["capital"] >= 200:
                    state["capital"] -= 200
                    state["raw_materials"] += 150
                    state["major_action_taken"] = True
                    print("\nEmergency bulk import successful! Acquired +150 Raw Materials for $200.")
                else:
                    print("\n[!] Insufficient Capital! Emergency import requires $200.")

            input("\nPress Enter to return to the dashboard...")

        # Handle Minor Actions Sub-Menu [6]
        elif choice == "6":
            if state["minor_actions_used"] >= state["max_minor_actions"]:
                clear_screen()
                input("\n[!] You have no Minor Actions left this month! Press Enter.")
                continue

            clear_screen()
            print("=" * 65)
            print("               🛠️ TACTICAL MINOR ACTIONS MENU               ")
            print("=" * 65)
            print(" Select Category:")
            print("   [1] Operations")
            print("   [2] Maintenance")
            print("   [3] Market")
            print("   [4] Logistics")
            print("   [5] Human Capital")
            print("   [6] Return")
            print("-" * 65)

            cat = input("Select category (1-6): ").strip()
            if cat in ["1", "2", "3", "4", "5"]:
                state["minor_actions_used"] += 1
                clear_screen()
                print(f"\n[Tactical Action Executed Successfully for Category {cat}]")
                input("\nPress Enter to return to dashboard...")

        # Handle Sales Contract [7]
        elif choice == "7":
            if state["minor_actions_used"] >= state["max_minor_actions"]:
                clear_screen()
                input("\n[!] You have no Minor Actions left this month! Press Enter.")
                continue

            state["minor_actions_used"] += 1
            clear_screen()
            print(f"--- MONTH {state['current_month']}: SALES CONTRACT EXECUTION ---")

            if state["finished_goods"] > 0:
                state, earned, sold = execute_sales_contract(state, state["finished_goods"])
                print(f"\n Successfully sold {sold} units for ${earned:.2f}.")
                if state["finished_goods"] > 0:
                    print(f" Note: {state['finished_goods']} excess units remain in warehouse.")
            else:
                print("\n[!] No finished goods available in inventory to sell.")
            input("\nPress Enter to return to the dashboard...")

        # Handle System Controls / End Month [8]
        elif choice == "8" or (
                (state["major_action_taken"] or state["skip_next_major"]) and state["minor_actions_used"] >= state[
            "max_minor_actions"]):
            clear_screen()
            print(f"=== END OF MONTH {state['current_month']} SUMMARY ===")

            cave_in = state["research_levels"]["efficiency"] >= 4 and random.random() < state["negative_event_chance"]
            state = process_end_of_month_rollover(state, cave_in)

            if cave_in:
                print(" [CAVE IN HAZARD!]: Deep drilling disaster! -$90 incurred and monthly raw materials lost.")

            print("\n Advancing time cycle...\n")
            input("\nPress Enter to begin the new month...")

        elif choice == "9":
            clear_screen()
            print(f"\nExiting {state['difficulty_name']} simulation. Thanks for playing CliFactory!")
            break
        else:
            clear_screen()
            input("\n[!] Invalid choice. Press Enter to try again.")


if __name__ == "__main__":
    run_game()