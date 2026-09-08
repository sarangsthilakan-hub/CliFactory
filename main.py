import os
import random


def clear_screen():
    # Clears the terminal screen across Windows, Mac, and Linux
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
    diff_name, capital, guaranteed_months = select_difficulty()

    # Game State Variables
    current_month = 1
    raw_materials = 20
    finished_goods = 0

    # Factory Production Parameters
    base_passive_mining = 25
    base_passive_refining = 18
    factory_expansion_levels = 0
    base_maintenance_cost = 50
    expansion_cost = 300

    # Progressive Factory Naming List
    factory_tiers_names = [
        "Factory",
        "Large Factory",
        "Large Factory Complex",
        "Mega Factory",
        "Mega Factory Supercomplex",
        "Ultra-Industrial Zenith Complex",
    ]

    max_sell_limit = 50

    # Futures Contract Quota Tracking
    futures_contract_active = False
    futures_quota_target = 40  # Balanced quota target for the month

    skip_next_major = False

    # Global Market & Sales Tracking
    market_price_multiplier = 20.0
    total_goods_sold_this_month = 0

    # Multi-Tier R&D Tech Trees & Dynamic Risk Tracking
    research_levels = {
        "logistics": 0,
        "efficiency": 0,
        "safety": 0,
        "marketing": 0,
    }
    negative_event_chance = 0.25

    # Turn tracking constraints
    major_action_taken = False
    max_minor_actions = 2
    minor_actions_used = 0

    while True:
        # Check Loss Condition (Bankruptcy)
        if capital <= 0:
            clear_screen()
            print("=" * 75)
            print(
                "                     💀 GAME OVER: BANKRUPTCY 💀                     "
            )
            print("=" * 75)
            print(f" Month Reached: {current_month}")
            print(
                " Capital reserves have hit $0. Your corporate board has voted to liquidate"
            )
            print(
                " assets, and your company has been acquired in a hostile buyout. You"
            )
            print(" are officially no longer the CEO.")
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        # Check Victory Condition (Monopoly)
        total_output_rate = base_passive_refining + (
                factory_expansion_levels * 15
        )
        if capital >= 10000.0 and total_output_rate >= 100:
            clear_screen()
            print("=" * 75)
            print(
                "                   👑 VICTORY: GLOBAL MONOPOLY 👑                    "
            )
            print("=" * 75)
            print(f" Month Reached: {current_month}")
            print(f" Final Capital: ${capital:.2f}")
            print(f" Monthly Production Output: {total_output_rate} goods/mo")
            print(
                " Extraordinary work! You have completely crushed all market competition,"
            )
            print(
                " achieved absolute supply-chain dominance, and established a global monopoly."
            )
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        clear_screen()

        current_factory_title = factory_tiers_names[
            min(factory_expansion_levels, len(factory_tiers_names) - 1)
        ]

        # Top Header
        header_left = f"🏭 CLIFACTORY [{diff_name.upper()}]"
        header_right = f"📅 MONTH: {current_month}"
        print("=" * 75)
        print(f"{header_left:<45}{header_right:>28}")
        print("=" * 75)

        # Status Panel
        print(f" Facility Scale: [{current_factory_title}] (Level {factory_expansion_levels})")
        print(
            f" Capital: ${capital:.2f}  |  Raw Materials: {raw_materials}"
            f"  |  Finished Goods: {finished_goods}"
        )
        print(
            f" Upkeep: ${base_maintenance_cost}/mo  |  Max Sell Limit:"
            f" {max_sell_limit} units/contract"
        )
        print(
            f" Tech Tiers -> Logistics: {research_levels['logistics']}/4 |"
            f" Efficiency: {research_levels['efficiency']}/4 | Safety:"
            f" {research_levels['safety']}/4 | Marketing:"
            f" {research_levels['marketing']}/4"
        )

        if current_month <= guaranteed_months:
            print(
                " Status: 🛡️ Guaranteed Positive Outcome Active"
                f" ({guaranteed_months - current_month + 1} months left)"
            )
        else:
            print(" Status: ⚠️ Standard Market Risk Active")

        if futures_contract_active:
            print(
                f" Status Alert: 📈 Corporate Futures Contract Active (Quota: {futures_quota_target} goods | Bonus: 2.5x Price)")

        if skip_next_major:
            print(
                " Status Alert: 🔴 Major Action locked due to prior failure!"
            )

        print(
            f" Actions Left this Month -> Major: "
            f"{'0/1 (Done/Locked)' if (major_action_taken or skip_next_major) else '1 Available'}"
            f" | Minor: {max_minor_actions - minor_actions_used}/{max_minor_actions}"
        )
        print("-" * 75)

        # Menu Interface
        print(" CHOOSE YOUR ACTIONS:")
        print("\n [MAJOR ACTIONS (Max 1 per month)]")
        if not major_action_taken and not skip_next_major:
            print(
                "   [1] Prospect Unknown Sector (Exploration: High risk / reward pool)"
            )
            print(
                f"   [2] Construct Factory Expansion (Expansion: -${expansion_cost} Cap)"
            )
            print(
                "   [3] Invest in R&D (Logistics, Efficiency, Safety, Marketing)"
            )
            print(
                f"   [4] Corporate Futures Contract (Commit to selling {futures_quota_target}+ goods for massive profit)"
            )
            print(
                "   [5] Bulk Material Import (Supply Chain: Emergency +150 Raw for $200)"
            )
        else:
            print(
                "   [1-5] (Major Action unavailable or completed this month)"
            )

        print("\n [MINOR ACTIONS (Limited per month)]")
        print("   [6] Secure Sales Contract & Sell Finished Goods on Market")
        print("   [7] Oversee operations & adjust logistics workflows")

        print("\n [SYSTEM CONTROLS]")
        print("   [8] End Month Early & Proceed to Next Cycle")
        print("   [9] Quit Game")
        print("-" * 75)

        choice = input("Select an option (1-9): ").strip()

        # Action Handlers
        if choice in ["1", "2", "3", "4", "5"]:
            if major_action_taken or skip_next_major:
                clear_screen()
                if skip_next_major:
                    print(
                        "\n[!] Major Action is locked this month due to prior failure!"
                    )
                else:
                    print(
                        "\n[!] You have already performed your Major Action this month!"
                    )
                input("Press Enter to continue.")
                continue

            major_action_taken = True
            clear_screen()

            # --- 1. PROSPECT UNKNOWN SECTOR ---
            if choice == "1":
                print(
                    f"--- MONTH {current_month}: PROSPECT UNKNOWN SECTOR ---"
                )

                if current_month <= guaranteed_months:
                    event_roll = random.choice(["high_yield", "geode", "shaft"])
                else:
                    current_hazard_chance = max(
                        0.05,
                        negative_event_chance
                        - (research_levels["safety"] * 0.05),
                    )

                    roll_type = random.random()
                    if roll_type < current_hazard_chance:
                        event_roll = random.choice(
                            ["gas", "seepage", "slip", "insects"]
                        )
                    elif roll_type < current_hazard_chance + 0.35:
                        event_roll = random.choice(
                            ["high_yield", "unstable", "shaft", "geode"]
                        )
                    else:
                        event_roll = random.choice(["barren", "cavern"])

                if event_roll == "high_yield":
                    raw_materials += 75
                    print(
                        "\n [Success]: Located a rich rare mineral vein. (+75 Raw Materials)"
                    )
                elif event_roll == "unstable":
                    print(
                        "\n [Discovery]: Encountered Unstable Soil formations."
                    )
                    sub_choice = input(
                        "   Keep digging deeper [1] or Cease operations [2]? "
                    ).strip()
                    if sub_choice == "1":
                        if random.random() < 0.5:
                            raw_materials += 125
                            print(
                                "\n [Deep Dig Success]: Uncovered untouched mineral pockets! (+125 Raw Materials)"
                            )
                        else:
                            capital -= 40
                            print(
                                "\n [Cave-in Hazard]: Deep trench collapsed! Minor equipment damage cost -$40."
                            )
                    else:
                        print(
                            "\n [Safe Call]: Ceased operations safely. No resources gained or lost."
                        )
                elif event_roll == "geode":
                    capital += 300
                    print(
                        "\n [JACKPOT!]: Uncovered a magnificent geode of precious gemstones! (+300 Capital)"
                    )
                elif event_roll == "shaft":
                    raw_materials += 90
                    print(
                        "\n [Salvage]: Stumbled upon an abandoned colonial mining cache with sealed crates. (+90 Raw Materials)"
                    )
                elif event_roll == "barren":
                    print(
                        "\n [Dead End]: The exploration team scans a sprawling sector of completely dead rock. Finds nothing of importance."
                    )
                elif event_roll == "cavern":
                    print(
                        "\n [Hollow Earth]: The sector yields an empty network of hollow rock formations. Finds nothing of importance."
                    )
                elif event_roll == "gas":
                    capital -= 30
                    print(
                        "\n [Hazard]: Drilling punctured a minor pocket of foul, corrosive gas. Quick filter replacements cost -$30."
                    )
                elif event_roll == "seepage":
                    capital -= 40
                    print(
                        "\n [Hazard]: Breaking through a wall caused minor water seepage into the trench. Pumping equipment cost -$40."
                    )
                elif event_roll == "slip":
                    capital -= 45
                    print(
                        "\n [Hazard]: A minor rockshift settled the walls, misaligning drilling gear. Alignment touch-ups cost -$45."
                    )
                elif event_roll == "insects":
                    capital -= 35
                    print(
                        "\n [Hazard]: Crews disturbed subterranean pests that chewed through wiring. Harness repairs cost -$35."
                    )

            # --- 2. CONSTRUCT FACTORY EXPANSION ---
            elif choice == "2":
                print(
                    f"--- MONTH {current_month}: CONSTRUCT FACTORY EXPANSION ---"
                )
                if capital >= expansion_cost:
                    print(f"Expansion Cost: ${expansion_cost}")
                    print("Select your factory expansion focus strategy:\n")
                    print("  [1] Ruthless Efficiency")
                    print("      - Output Boost: High (+20 refining capacity)")
                    print("      - Maintenance Cost: Small increase (+$15/mo)")
                    print("      - Safety Impact: Increases negative event chance (+6% risk)\n")
                    print("  [2] Safety-First Focus")
                    print("      - Output Boost: Moderate (+10 refining capacity)")
                    print("      - Maintenance Cost: Moderate increase (+$25/mo)")
                    print("      - Safety Impact: Significantly improves safety (-12% risk)\n")
                    print("  [3] Cost-Cutting Focus")
                    print("      - Output Boost: High (+15 refining capacity)")
                    print("      - Maintenance Cost: Very low increase (+$5/mo)")
                    print("      - Safety Impact: Significantly increases negative event chance (+15% risk)")

                    strat_choice = input("\nSelect strategy (1-3): ").strip()

                    capital -= expansion_cost
                    factory_expansion_levels += 1

                    if strat_choice == "1":
                        base_maintenance_cost += 15
                        negative_event_chance += 0.06
                        print(
                            "\n[Ruthless Efficiency Applied]: Factory expanded! Maintenance increased by +$15/mo, negative event risk increased by +6%."
                        )
                    elif strat_choice == "2":
                        base_maintenance_cost += 25
                        negative_event_chance = max(0.01, negative_event_chance - 0.12)
                        print(
                            "\n[Safety Focus Applied]: Factory expanded! Maintenance increased by +$25/mo, safety improved significantly (-12% risk)."
                        )
                    elif strat_choice == "3":
                        base_maintenance_cost += 5
                        negative_event_chance += 0.15
                        print(
                            "\n[Cost-Cutting Focus Applied]: Factory expanded! Maintenance increased by only +$5/mo, but negative event risk increased sharply (+15% risk)."
                        )
                    else:
                        base_maintenance_cost += 20
                        print(
                            "\n[Standard Expansion Applied]: Factory expanded with balanced defaults."
                        )
                else:
                    print(
                        f"\n[!] Insufficient Capital! Construction requires ${expansion_cost}."
                    )
                    major_action_taken = False

            # --- 3. INVEST IN R&D ---
            elif choice == "3":
                print(f"--- MONTH {current_month}: RESEARCH & DEVELOPMENT ---")
                print("Select a research field to invest in (-$100 Funds):")
                print(
                    f"  [1] Logistics [Tier: {research_levels['logistics']}/4]"
                )
                print(
                    f"  [2] Efficiency [Tier: {research_levels['efficiency']}/4]"
                )
                print(f"  [3] Safety [Tier: {research_levels['safety']}/4]")
                print(
                    f"  [4] Marketing [Tier: {research_levels['marketing']}/4]"
                )
                print("  [5] Cancel R&D Investment")

                rd_choice = input("\nSelect field (1-5): ").strip()

                if rd_choice in ["1", "2", "3", "4"]:
                    field_map = {
                        "1": "logistics",
                        "2": "efficiency",
                        "3": "safety",
                        "4": "marketing",
                    }
                    selected_field = field_map[rd_choice]

                    if research_levels[selected_field] >= 4:
                        print(
                            "\n[!] All technologies for this field are already fully researched! No more research can be done here."
                        )
                        major_action_taken = False
                    elif capital >= 100:
                        capital -= 100
                        research_levels[selected_field] += 1
                        tier = research_levels[selected_field]

                        fail_chance = (
                            0.0
                            if (
                                    current_month <= guaranteed_months
                                    or selected_field == "marketing"
                            )
                            else 0.05
                        )
                        if random.random() < fail_chance:
                            research_levels[selected_field] -= 1
                            print(
                                "\n[!] RESEARCH FAILURE! -$100 funds wasted with no technology unlocked."
                            )
                        else:
                            if selected_field == "logistics":
                                if tier == 1:
                                    base_maintenance_cost = max(
                                        0, base_maintenance_cost - 5
                                    )
                                    print(
                                        "\n[Tech 1/4 Unlocked] Advanced Logistics: Maintenance $5 cheaper."
                                    )
                                elif tier == 2:
                                    max_sell_limit += 20
                                    base_maintenance_cost += 10
                                    print(
                                        "\n[Tech 2/4 Unlocked] Transport Planes: +20% profit, max sell limit +20, maintenance +$10."
                                    )
                                elif tier == 3:
                                    max_sell_limit += 50
                                    base_maintenance_cost += 5
                                    print(
                                        "\n[Tech 3/4 Unlocked] Sea Freight: +10% profit, max sell limit +50, maintenance +$5."
                                    )
                                elif tier == 4:
                                    base_maintenance_cost = max(
                                        0, base_maintenance_cost - 15
                                    )
                                    print(
                                        "\n[Tech 4/4 Unlocked] Improved Warehouses: Maintenance reduced by $15."
                                    )
                            elif selected_field == "efficiency":
                                if tier == 1:
                                    base_maintenance_cost += 5
                                    print(
                                        "\n[Tech 1/4 Unlocked] Improved Tools: +5 finished goods/mo, maintenance +$5."
                                    )
                                elif tier == 2:
                                    base_maintenance_cost -= 5
                                    expansion_cost += 20
                                    print(
                                        "\n[Tech 2/4 Unlocked] High Quality Equipment: +10 goods/mo, maintenance -$5, expansion +$20."
                                    )
                                elif tier == 3:
                                    print(
                                        "\n[Tech 3/4 Unlocked] Automated Equipment: Raw +20, finished +5."
                                    )
                                elif tier == 4:
                                    print(
                                        "\n[Tech 4/4 Unlocked] Deep Drilling: Raw +35 (Unlocks 'cave in' risk)."
                                    )
                            elif selected_field == "safety":
                                if tier == 1:
                                    base_maintenance_cost += 3
                                    print(
                                        "\n[Tech 1/4 Unlocked] Basic Hazard Protocols: Exploration hazard risk reduced, upkeep +$3."
                                    )
                                elif tier == 2:
                                    base_maintenance_cost += 4
                                    print(
                                        "\n[Tech 2/4 Unlocked] Reinforced Flooring: Hazard risk further reduced, upkeep +$4."
                                    )
                                elif tier == 3:
                                    base_maintenance_cost += 5
                                    print(
                                        "\n[Tech 3/4 Unlocked] Autonomous Fire Suppression: Hazard risk significantly lowered, upkeep +$5."
                                    )
                                elif tier == 4:
                                    base_maintenance_cost += 6
                                    print(
                                        "\n[Tech 4/4 Unlocked] Zero-Incident AI Grid: Near total accident suppression, upkeep +$6."
                                    )
                            elif selected_field == "marketing":
                                if tier == 1:
                                    print(
                                        "\n[Tech 1/4 Unlocked] Regional Advertising: Quota 50 goods (+5% bonus)."
                                    )
                                elif tier == 2:
                                    print(
                                        "\n[Tech 2/4 Unlocked] National Distribution: Quota 70 goods (+10% bonus)."
                                    )
                                elif tier == 3:
                                    print(
                                        "\n[Tech 3/4 Unlocked] Continental Brand: Quota 90 goods (+15% bonus)."
                                    )
                                elif tier == 4:
                                    print(
                                        "\n[Tech 4/4 Unlocked] Global Monopoly Campaign: Quota 120 goods (+25% bonus)."
                                    )
                    else:
                        print(
                            "\n[!] Insufficient Capital! R&D investment requires $100."
                        )
                        major_action_taken = False
                else:
                    print("\n[!] R&D action canceled. Major action refunded.")
                    major_action_taken = False

            # --- 4. CORPORATE FUTURES CONTRACT ---
            elif choice == "4":
                print(
                    f"--- MONTH {current_month}: CORPORATE FUTURES CONTRACT ---"
                )
                futures_contract_active = True
                print(
                    f"\n Secured futures contract! Target quota for this month is {futures_quota_target} goods."
                    f" If you sell {futures_quota_target}+ goods this month, you will receive a massive 2.5x profit multiplier."
                    f" If you fail to meet the quota by month end, you will incur a -10% capital penalty."
                )

            # --- 5. BULK MATERIAL IMPORT ---
            elif choice == "5":
                print(f"--- MONTH {current_month}: BULK MATERIAL IMPORT ---")
                if capital >= 200:
                    capital -= 200
                    raw_materials += 150
                    print(
                        "\n Emergency bulk import successful! Purchased +150 Raw Materials for $200."
                    )
                else:
                    print(
                        "\n[!] Insufficient Capital! Emergency bulk import requires $200."
                    )
                    major_action_taken = False

            input("\nPress Enter to return to the dashboard...")

        elif choice == "6":
            if minor_actions_used >= max_minor_actions:
                clear_screen()
                input(
                    "\n[!] You have no Minor Actions left this month! Press Enter to continue."
                )
                continue
            minor_actions_used += 1
            clear_screen()
            print(f"--- MONTH {current_month}: SALES CONTRACT EXECUTION ---")

            current_unit_price = market_price_multiplier
            if research_levels["logistics"] >= 2:
                current_unit_price *= 1.20
            if research_levels["logistics"] >= 3:
                current_unit_price *= 1.10

            if finished_goods > 0:
                sold_amount = min(finished_goods, max_sell_limit)

                # Apply 2.5x futures multiplier if contract is active
                if futures_contract_active:
                    current_unit_price *= 2.5
                    print(" [Futures Contract Active]: Applying 2.5x price multiplier bonus!")

                earned = sold_amount * current_unit_price
                capital += earned
                finished_goods -= sold_amount
                total_goods_sold_this_month += sold_amount

                print(
                    f"\n Successfully sold {sold_amount} units (limit {max_sell_limit}) for ${earned:.2f}."
                )
                if finished_goods > 0:
                    print(
                        f" Note: {finished_goods} excess units remain in warehouse."
                    )
            else:
                print(
                    "\n[!] No finished goods available in inventory to sell."
                )
            input("\nPress Enter to return to the dashboard...")

        elif choice == "7":
            if minor_actions_used >= max_minor_actions:
                clear_screen()
                input(
                    "\n[!] You have no Minor Actions left this month! Press Enter to continue."
                )
                continue
            minor_actions_used += 1
            clear_screen()
            print(f"--- MONTH {current_month}: OPERATIONS AUDIT ---")
            capital += 50
            print(
                "\n Routine infrastructure audit completed. Recovered $50 in overhead savings."
            )
            input("\nPress Enter to return to the dashboard...")

        elif choice == "8" or (
                (major_action_taken or skip_next_major)
                and minor_actions_used >= max_minor_actions
        ):
            clear_screen()
            print(f"=== END OF MONTH {current_month} SUMMARY ===")

            # --- EVALUATE CORPORATE FUTURES QUOTA ---
            if futures_contract_active:
                if total_goods_sold_this_month >= futures_quota_target:
                    print(
                        f" [Futures Contract Met]: Sold {total_goods_sold_this_month} / {futures_quota_target} required goods. Contract fulfilled successfully with massive bonuses!"
                    )
                else:
                    penalty_amount = capital * 0.10
                    capital -= penalty_amount
                    print(
                        f" [Futures Contract Failed]: Sold only {total_goods_sold_this_month} / {futures_quota_target} required goods. Penalty incurred: -10% capital (-${penalty_amount:.2f})."
                    )
                futures_contract_active = False

            # Marketing Quotas Check
            marketing_tier = research_levels["marketing"]
            quota_targets = {
                1: (50, 0.05),
                2: (70, 0.10),
                3: (90, 0.15),
                4: (120, 0.25),
            }
            if marketing_tier > 0:
                q_target, q_bonus = quota_targets[marketing_tier]
                if total_goods_sold_this_month >= q_target:
                    bonus_cash = capital * q_bonus
                    capital += bonus_cash
                    print(
                        f" [Marketing Quota Met]: Sold {total_goods_sold_this_month} / {q_target}! Awarded +{int(q_bonus * 100)}% profit bonus (${bonus_cash:.2f})."
                    )
                else:
                    print(
                        f" [Marketing Quota Missed]: Sold {total_goods_sold_this_month} / {q_target} for Tier {marketing_tier}."
                    )

            # Passive Mining & Refining Cycle
            eff_tier = research_levels["efficiency"]
            mining_bonus = 0
            refining_bonus = 0
            if eff_tier >= 3:
                mining_bonus += 20
                refining_bonus += 5
            if eff_tier >= 4:
                mining_bonus += 35

            total_mined = (
                    base_passive_mining
                    + (factory_expansion_levels * 5)
                    + mining_bonus
            )

            cave_in_occurred = False
            active_event_chance = max(
                0.01,
                negative_event_chance - (research_levels["safety"] * 0.03),
            )
            if eff_tier >= 4 and random.random() < active_event_chance:
                cave_in_occurred = True
                capital -= 90
                total_mined = 0
                print(
                    " [CAVE IN HAZARD!]: Deep drilling disaster! -$90 incurred and all raw material this month is lost."
                )

            if not cave_in_occurred:
                raw_materials += total_mined
                print(
                    f" Autonomous extraction mined +{total_mined} raw materials."
                )

            total_refined_capacity = (
                    base_passive_refining
                    + (factory_expansion_levels * 15)
                    + refining_bonus
            )
            if eff_tier >= 1:
                total_refined_capacity += 5
            if eff_tier >= 2:
                total_refined_capacity += 10

            actual_refined = min(raw_materials, total_refined_capacity)
            raw_materials -= actual_refined
            finished_goods += actual_refined
            print(
                f" Factory converted {actual_refined} raw materials into finished goods."
            )

            capital -= base_maintenance_cost
            print(
                f" Deducted ${base_maintenance_cost} monthly infrastructure maintenance."
            )

            print(
                f"\n Advancing time cycle to Month {current_month + 1}...\n"
            )

            current_month += 1
            major_action_taken = False
            skip_next_major = False
            minor_actions_used = 0
            total_goods_sold_this_month = 0

            input("\nPress Enter to begin the new month...")

        elif choice == "9":
            clear_screen()
            print(
                f"\nExiting {diff_name} simulation. Thanks for playing CliFactory!"
            )
            break
        else:
            clear_screen()
            input("\n[!] Invalid choice. Press Enter to try again.")


if __name__ == "__main__":
    run_game()