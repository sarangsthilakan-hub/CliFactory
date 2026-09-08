import os
import random
from factory_logic import (
    create_initial_game_state,
    is_bankrupt,
    has_achieved_monopoly,
    get_current_factory_title,
    calculate_effective_risk,
    evaluate_minor_action_risk,
    execute_factory_expansion,
    execute_rd_investment,
    execute_sales_contract,
    roll_monthly_event,
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
        print("       - Starting Capital: $800.00 | Goal: $5,000 & 50 goods/mo")
        print("\n   [2] MID-MARKET (Normal)")
        print("       - Starting Capital: $500.00 | Goal: $15,000, 120 goods/mo & 2 Max Techs")
        print("\n   [3] HOSTILE TAKEOVER (Hard)")
        print("       - Starting Capital: $250.00 | Goal: $35,000, 250 goods/mo, All Techs & 3 Futures")
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


def handle_monthly_event(state):
    is_positive, event_key = roll_monthly_event(state)
    if not event_key:
        return state

    clear_screen()
    print("=" * 75)
    print(f"       🚨 MONTHLY EVENT: {event_key.upper().replace('_', ' ')} 🚨       ")
    print("=" * 75)

    if event_key == "high_demand":
        state["temporary_price_bonus"] = 1.5
        print("\n[Positive]: High Market Demand! Next sales contract receives a +50% price bonus.")

    elif event_key == "subsidy":
        print("\n[Positive]: Government Clean Energy Subsidy!")
        print("  [A] Accept clean-up infrastructure grant (+$60 Capital & permanent risk reduction)")
        print("  [B] Take immediate cash payout (+$150 Capital)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 60
            state["negative_event_chance"] = max(0.05, state["negative_event_chance"] - 0.05)
            print("\n-> Accepted grant: +$60 Capital, risk exposure reduced.")
        else:
            state["capital"] += 150
            print("\n-> Took cash payout: +$150 Capital.")

    elif event_key == "investor":
        print("\n[Positive]: External Investor Interest!")
        print("  [A] Issue shares for funding (+$250 Capital)")
        print("  [B] Decline and protect equity")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 250
            print("\n-> Issued shares: +$250 Capital.")
        else:
            print("\n-> Declined investor backing.")

    elif event_key == "surplus":
        print("\n[Positive]: Warehouse Liquidation Sale!")
        print("  [A] Purchase surplus stock (+60 Raw Materials for $30)")
        print("  [B] Pass on the offer")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A" and state["capital"] >= 30:
            state["capital"] -= 30
            state["raw_materials"] += 60
            print("\n-> Purchased surplus: +60 Raw Materials for -$30.")
        else:
            print("\n-> Passed on liquidation deal.")

    elif event_key == "innovation":
        print("\n[Positive]: Star Employee Innovation!")
        print("  [A] File a commercial patent (+$100 Capital)")
        print("  [B] Distribute team bonuses (+10% yield on next Major Action)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 100
            print("\n-> Filed patent: +$100 Capital.")
        else:
            state["next_major_yield_bonus"] += 0.10
            print("\n-> Distributed bonuses: Next Major Action boosted by +10%.")

    elif event_key == "logistics_breakthrough":
        state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] // 2)
        print("\n[Positive]: Logistics Industry Breakthrough! Upkeep maintenance halved for this month.")

    elif event_key == "scrap_boom":
        print("\n[Positive]: Scrap Metal Market Boom!")
        print("  [A] Sell factory scrap reserves (+$120 Capital)")
        print("  [B] Melt scrap down into raw material (+40 Raw Materials)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 120
            print("\n-> Sold scrap: +$120 Capital.")
        else:
            state["raw_materials"] += 40
            print("\n-> Melted scrap: +40 Raw Materials.")

    elif event_key == "espionage_windfall":
        print("\n[Positive]: Corporate Espionage Windfall! Acquired open intel.")
        state["capital"] += 80
        print("-> Secured trade secrets: +$80 Capital.")

    elif event_key == "angel_investor":
        print("\n[Positive]: Angel Investor Syndicate!")
        print("  [A] Accept equity loan (+$300 Capital, +$15 monthly interest)")
        print("  [B] Take outright grant (+$120 Capital)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 300
            state["base_maintenance_cost"] += 15
            print("\n-> Loan accepted: +$300 Capital, +$15 monthly upkeep increase.")
        else:
            state["capital"] += 120
            print("\n-> Grant accepted: +$120 Capital.")

    elif event_key == "award":
        state["capital"] += 200
        state["market_price_multiplier"] += 2.0
        print("\n[Positive]: State Industrial Excellence Award! +$200 Capital and brand value increased.")

    elif event_key == "supply_surplus":
        state["raw_materials"] += 50
        print("\n[Positive]: Bulk Supply Surplus Delivery! Received +50 Raw Materials free.")

    elif event_key == "merger":
        print("\n[Positive]: Friendly Corporate Merger Offer!")
        print("  [A] Absorb assets (+30 Finished Goods, -$80 fee)")
        print("  [B] Decline")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A" and state["capital"] >= 80:
            state["capital"] -= 80
            state["finished_goods"] += 30
            print("\n-> Merged assets: +30 Finished Goods for -$80.")
        else:
            print("\n-> Decline merger offer.")

    elif event_key == "tech_leak":
        state["capital"] += 90
        print("\n[Positive]: Technological Breakthrough Leak! R&D efficiency insights grant +$90 Capital.")

    elif event_key == "drone_gift":
        state["max_sell_limit"] += 15
        print("\n[Positive]: Autonomous Drone Delivery Gift! Max sell limit permanently increased by +15.")

    elif event_key == "grid_rebate":
        state["capital"] += 90
        print("\n[Positive]: Energy Grid Rebate! Municipal utility rewards efficiency with +$90 Capital.")

    elif event_key == "patent_buyout":
        print("\n[Positive]: Secret Patent Buyout!")
        print("  [A] Sell blueprint outright (+$180 Capital)")
        print("  [B] Retain rights (+15 Capital every month)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] += 180
            print("\n-> Sold patent outright: +$180 Capital.")
        else:
            state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] - 15)
            print("\n-> Retained rights: Monthly maintenance permanently reduced by -$15.")

    elif event_key == "skilled_labor":
        print("\n[Positive]: Skilled Labor Influx!")
        print("  [A] Hire expert engineers (+10 refining capacity, +$15 wage upkeep)")
        print("  [B] Pass")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["base_maintenance_cost"] += 15
            print("\n-> Hired engineers: Upkeep increased by +$15, refining output boosted.")
        else:
            print("\n-> Passed on hiring.")

    elif event_key == "luxury_contract":
        state["temporary_price_bonus"] = 2.0
        print("\n[Positive]: Luxury Commercial Contract! Next sales contract receives a double-value multiplier.")

    elif event_key == "tax_loophole":
        state["capital"] += 100
        print("\n[Positive]: Tax Loophole Discovery! Accountants refund +$100 Capital.")

    elif event_key == "trade_treaty":
        print("\n[Positive]: Global Trade Treaty Realignment! Bulk Material Imports permanently discounted by $50.")

    # --- NEGATIVE EVENTS HANDLING ---
    elif event_key == "strike":
        print("\n[Negative]: Worker Strikes!")
        print("  [A] Negotiate living wages (+10 permanent monthly maintenance)")
        print("  [B] Fire striking workers (Reduce refining capacity by -5 for the month)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["base_maintenance_cost"] += 10
            print("\n-> Negotiated wages: Maintenance increased by +$10/mo.")
        else:
            state["temporary_refining_modifier"] -= 5
            print("\n-> Fired workers: Refining capacity reduced by -5 for this month.")

    elif event_key == "audit":
        print("\n[Negative]: Regulatory Safety Audit!")
        print("  [A] Pay immediate compliance fine (-$80 Capital)")
        print("  [B] Contest in court (50% chance to pay $0, 50% chance to pay -$160)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 80
            print("\n-> Paid fine: -$80 Capital.")
        else:
            if random.random() < 0.50:
                print("\n-> Court ruling successful! Infractions dismissed with $0 penalty.")
            else:
                state["capital"] -= 160
                print("\n-> Court ruling failed! Heavy penalty incurred: -$160 Capital.")

    elif event_key == "brownout":
        state["temporary_refining_modifier"] -= 8
        print("\n[Negative]: Power Grid Brownout! Refining output throttled for the month.")

    elif event_key == "contamination":
        spoiled = min(state["raw_materials"], 35)
        state["raw_materials"] -= spoiled
        print(f"\n[Negative]: Warehouse Contamination! Spoilage destroyed {spoiled} Raw Materials.")

    elif event_key == "circuit":
        print("\n[Negative]: Machinery Short-Circuit!")
        print("  [A] Professional emergency repairs (-$70 Capital)")
        print("  [B] Makeshift wiring (+$20 permanent maintenance friction drag)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 70
            print("\n-> Professional repairs paid: -$70 Capital.")
        else:
            state["base_maintenance_cost"] += 20
            print("\n-> Makeshift patch applied: Maintenance increased by +$20/mo.")

    elif event_key == "piracy":
        print("\n[Negative]: Supply Chain Piracy / Hijacking!")
        print("  [A] Hire private security escort (-$50 Capital, blocks future transit thefts)")
        print("  [B] Write off the loss (-40 Raw Materials)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 50
            print("\n-> Hired security: -$50 Capital. Convoy secured.")
        else:
            state["raw_materials"] = max(0, state["raw_materials"] - 40)
            print("\n-> Wrote off loss: Lost 40 Raw Materials.")

    elif event_key == "chemical_leak":
        print("\n[Negative]: Corrosive Chemical Leak!")
        print("  [A] Hazmat cleanup crew (-$90 Capital)")
        print("  [B] Internal cleanup (-15 Finished Goods inventory spoiled)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 90
            print("\n-> Hazmat crew paid: -$90 Capital.")
        else:
            state["finished_goods"] = max(0, state["finished_goods"] - 15)
            print("\n-> Internal cleanup: Lost 15 Finished Goods.")

    elif event_key == "tax_hike":
        print("\n[Negative]: Municipal Property Tax Hike!")
        print("  [A] Pay increased tax (+$15 permanent monthly maintenance)")
        print("  [B] File legal appeals (-$50 legal fee, 50% chance to block hike)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["base_maintenance_cost"] += 15
            print("\n-> Paid tax hike: Maintenance increased by +$15/mo.")
        else:
            state["capital"] -= 50
            if random.random() < 0.50:
                print("\n-> Legal appeal successful! Tax hike blocked.")
            else:
                state["base_maintenance_cost"] += 15
                print("\n-> Appeal failed. Paid $50 fee and tax hike applied anyway.")

    elif event_key == "subcontractor_drop":
        print("\n[Negative]: Subcontractor Bankruptcy!")
        print("  [A] Emergency contract buyout (-$110 Capital)")
        print("  [B] Suffer shipping bottlenecks (-20 max sell limit for month)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 110
            print("\n-> Buyout paid: -$110 Capital.")
        else:
            state["max_sell_limit"] = max(10, state["max_sell_limit"] - 20)
            print("\n-> Bottleneck accepted: Max sell limit reduced for the month.")

    elif event_key == "espionage_breach":
        print("\n[Negative]: Espionage Data Breach!")
        print("  [A] Upgrade firewall encryption (-$100 Capital)")
        print("  [B] Risk market undercutting (-10% sales prices for the month)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 100
            print("\n-> Firewall upgraded: -$100 Capital.")
        else:
            state["temporary_price_bonus"] *= 0.90
            print("\n-> Undercutting accepted: Sales prices reduced by 10% for the month.")

    elif event_key == "tremor":
        print("\n[Negative]: Subterranean Tremor!")
        print("  [A] Structural reinforcement engineering (-$120 Capital)")
        print("  [B] Ignore it (Permanently increases negative event risk by +5%)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 120
            print("\n-> Reinforcements built: -$120 Capital.")
        else:
            state["negative_event_chance"] = min(1.0, state["negative_event_chance"] + 0.05)
            print("\n-> Ignored: Permanent hazard risk increased by +5%.")

    elif event_key == "pension_deficit":
        print("\n[Negative]: Union Pension Deficit Charge!")
        print("  [A] Settle fully (-$140 Capital)")
        print("  [B] Defer payments (Triggers a minor strike event next month)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 140
            print("\n-> Pension settled: -$140 Capital.")
        else:
            state["temporary_refining_modifier"] -= 3
            print("\n-> Deferred: Workers staging slowdowns.")

    elif event_key == "counterfeit_ore":
        spoiled_raw = min(state["raw_materials"], 20)
        state["raw_materials"] -= spoiled_raw
        print(f"\n[Negative]: Counterfeit Raw Material Batch! Discovered bad ore, losing {spoiled_raw} Raw Materials.")

    elif event_key == "customs_delay":
        print("\n[Negative]: Customs Impound Delays!")
        print("  [A] Pay expedited clearance bribes (-$90 Capital)")
        print("  [B] Wait out delay (Halts incoming raw material deliveries for cycle)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 90
            print("\n-> Bribes paid: -$90 Capital. Clearance expedited.")
        else:
            print("\n-> Waited out delay: No raw materials will be mined/extracted next cycle.")
            state["temporary_refining_modifier"] -= 15

    elif event_key == "lawsuit":
        print("\n[Negative]: Workplace Injury Lawsuit!")
        print("  [A] Settle out of court (-$130 Capital)")
        print("  [B] Fight legally (-$60 legal fees, 40% chance of losing double)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 130
            print("\n-> Settled out of court: -$130 Capital.")
        else:
            state["capital"] -= 60
            if random.random() < 0.40:
                state["capital"] -= 200
                print("\n-> Lost court battle! Paid -$260 total.")
            else:
                print("\n-> Won court battle! Saved from massive liability.")

    elif event_key == "inflation":
        inflation_hit = state["capital"] * 0.05
        state["capital"] -= inflation_hit
        print(
            f"\n[Negative]: Currency Inflation Spike! National fiat devalues. Lost -${inflation_hit:.2f} to inflation.")

    elif event_key == "lightning":
        print("\n[Negative]: Substation Lightning Strike!")
        print("  [A] Replace hardware components (-$110 Capital)")
        print("  [B] Rework old circuit boards (Skip minor action availability for 1 turn)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 110
            print("\n-> Components replaced: -$110 Capital.")
        else:
            state["max_minor_actions"] = max(0, state["max_minor_actions"] - 1)
            print("\n-> Reworked manually: Minor actions restricted for the month.")

    elif event_key == "price_war":
        state["temporary_price_bonus"] *= 0.80
        print("\n[Negative]: Rival Corporate Price War! Competitors flood market. Sales prices reduced by 20%.")

    elif event_key == "union_slowdown":
        print("\n[Negative]: Logistics Union Slowdown!")
        print("  [A] Pay hazard bonuses to clear backlog (-$85 Capital)")
        print("  [B] Suffer logistics delays (Max sell limit halved)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 85
            print("\n-> Hazard bonuses paid: -$85 Capital.")
        else:
            state["max_sell_limit"] = state["max_sell_limit"] // 2
            print("\n-> Slowdown accepted: Max sell limit halved for the month.")

    elif event_key == "obsolescence":
        print("\n[Negative]: Obsolescence Crisis!")
        print("  [A] Re-tool production lines (-$150 Capital)")
        print("  [B] Sell at clearance discount (-20% revenue on sales)")
        choice = input("Select choice (A/B): ").strip().upper()
        if choice == "A":
            state["capital"] -= 150
            print("\n-> Re-tooled lines: -$150 Capital.")
        else:
            state["temporary_price_bonus"] *= 0.80
            print("\n-> Clearance discount accepted: -20% revenue penalty.")

    input("\nPress Enter to continue into the month...")
    return state


def run_game():
    diff_name, starting_capital, guaranteed_months = select_difficulty()
    state = create_initial_game_state(diff_name, starting_capital, guaranteed_months)

    while True:
        # Immediate mid-action bankruptcy check
        if is_bankrupt(state):
            clear_screen()
            print("=" * 75)
            print("                     💀 GAME OVER: BANKRUPTCY 💀                     ")
            print("=" * 75)
            print(f" Month Reached: {state['current_month']}")
            print(" Capital reserves have hit $0 or below. Hostile corporate buyout executed.")
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        if has_achieved_monopoly(state):
            clear_screen()
            print("=" * 75)
            print("                   👑 VICTORY: CORPORATE HEGEMONY 👑                   ")
            print("=" * 75)
            print(f" Difficulty Tier: {state['difficulty_name']}")
            print(f" Month Reached: {state['current_month']}")
            print(f" Final Capital: ${state['capital']:.2f}")
            print("=" * 75)
            input("\nPress Enter to exit CliFactory...")
            break

        clear_screen()

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
            print(
                f" Status Alert: 📈 Futures Contract Active (Quota: {state['futures_quota_target']} goods | Bonus: 2.5x Price)")

        if state["skip_next_major"]:
            print(" Status Alert: 🔴 Major Action locked due to prior failure!")

        major_exhausted = state["major_action_taken"] or state["skip_next_major"]
        minor_exhausted = state["minor_actions_used"] >= state["max_minor_actions"]

        print(
            f" Actions Left this Month -> Major: "
            f"{'0/1 (Done)' if major_exhausted else '1 Available'}"
            f" | Minor: {state['max_minor_actions'] - state['minor_actions_used']}/{state['max_minor_actions']}"
        )
        print("-" * 75)

        # Menu Interface with Dynamic Availability Hiding
        print(" CHOOSE YOUR ACTIONS:")
        print("\n [MAJOR ACTIONS (Max 1 per month)]")
        if not major_exhausted:
            print("   [1] Prospect Unknown Sector (Exploration)")
            print(f"   [2] Construct Factory Expansion (Structural upgrade: -${state['expansion_cost']} Cap)")
            print("   [3] Invest in R&D (Research Logistics, Efficiency, Safety, Marketing)")
            if state["futures_cooldown_remaining"] > 0:
                print(f"   [4] Corporate Futures Contract [ON COOLDOWN: {state['futures_cooldown_remaining']} mos]")
            else:
                print(f"   [4] Corporate Futures Contract (Commit to selling {state['futures_quota_target']}+ goods)")
            print("   [5] Bulk Material Import (Emergency supply chain: +150 Raw for $200)")
        else:
            print("   [1-5] [UNAVAILABLE - Major Action Completed or Locked]")

        print("\n [MINOR ACTIONS (Limited per month)]")
        if not minor_exhausted:
            print("   [6] Execute Tactical Minor Action (Operations, Maintenance, Market, Logistics, HR)")
            print("   [7] Secure Sales Contract & Sell Finished Goods on Market")
        else:
            print("   [6-7] [UNAVAILABLE - No Minor Actions Left This Month]")

        print("\n [SYSTEM CONTROLS]")
        if major_exhausted and minor_exhausted:
            print("   [8] 🟢 ALL ACTIONS EXHAUSTED - Proceed to Next Month")
        else:
            print("   [8] End Month Early & Proceed to Next Cycle")
        print("   [9] Quit Game")
        print("-" * 75)

        choice = input("Select an option (1-9): ").strip()

        # Handle Major Actions [1-5]
        if choice in ["1", "2", "3", "4", "5"]:
            if major_exhausted:
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
                    hazard_chance = calculate_effective_risk(state)
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
                print(f"--- MONTH {state['current_month']}: CORPORATE FUTURES CONTRACT ---")
                if state["futures_cooldown_remaining"] > 0:
                    print(
                        f"\n[!] Futures contract is on cooldown! ({state['futures_cooldown_remaining']} months remaining).")
                    state["major_action_taken"] = False
                else:
                    state["major_action_taken"] = True
                    state["futures_contract_active"] = True
                    state["futures_cooldown_remaining"] = 3
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
            if minor_exhausted:
                clear_screen()
                input("\n[!] You have no Minor Actions left this month! Press Enter to continue.")
                continue

            clear_screen()
            current_risk_pct = int(calculate_effective_risk(state) * 100)
            print("=" * 65)
            print(f"        🛠️ TACTICAL MINOR ACTIONS MENU (Risk: {current_risk_pct}%)       ")
            print("=" * 65)
            print(" Select Category:")
            print(f"   [1] Operations (Risk: {current_risk_pct}%)")
            print(f"   [2] Maintenance (Risk: {current_risk_pct}%)")
            print(f"   [3] Market (Risk: {current_risk_pct}%)")
            print(f"   [4] Logistics (Risk: {current_risk_pct}%)")
            print(f"   [5] Human Capital (Risk: {current_risk_pct}%)")
            print("   [6] Return to Dashboard")
            print("-" * 65)

            cat_choice = input("Select category (1-6): ").strip()

            if cat_choice == "1":
                if state["operations_locked_turns"] > 0:
                    input("\n[!] Operations is currently locked due to safety infractions! Press Enter.")
                    continue

                print("\n OPERATIONS ACTIONS:")
                print("   [1] Workflow Audit: Recovers +$30 Capital in savings.")
                print("   [2] Internal Line Shift: Converts 5 Raw to 3 Finished Goods instantly.")
                print("   [3] Energy Grid Calibration: Grants -$15 discount on next month's upkeep.")
                print("   [4] Speed Up Belt Feeders: +3 Finished Goods, but risks system jam (-5 Raw scrap).")
                print("   [5] Bypass Safety Checkpoints: Saves +$20 inspection fees, but risks locking Operations.")

                op_act = input("Select action (1-5): ").strip()
                state["minor_actions_used"] += 1
                clear_screen()

                if op_act == "1":
                    state["capital"] += 30
                    print("\n[Workflow Audit Successful]: Recovered +$30 Capital in operational savings.")
                elif op_act == "2":
                    if state["raw_materials"] >= 5:
                        state["raw_materials"] -= 5
                        state["finished_goods"] += 3
                        print("\n[Internal Line Shift Successful]: Converted 5 Raw Materials into 3 Finished Goods.")
                    else:
                        print("\n[Failed]: Not enough Raw Materials (need 5). Action wasted.")
                elif op_act == "3":
                    state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] - 15)
                    print("\n[Grid Calibration Successful]: Next month's upkeep discounted by -$15.")
                elif op_act == "4":
                    if evaluate_minor_action_risk(state):
                        if state["raw_materials"] >= 5:
                            state["raw_materials"] -= 5
                        state["finished_goods"] += 3
                        print(
                            f"\n[Belt Speeding Mishap (Risk Triggered)]: System jammed! Gained 3 goods but lost 5 Raw materials to scrap.")
                    else:
                        state["finished_goods"] += 3
                        print(
                            f"\n[Belt Speeding Safe]: Executed cleanly with zero scrap loss! Gained +3 Finished Goods.")
                elif op_act == "5":
                    if evaluate_minor_action_risk(state):
                        state["operations_locked_turns"] = 1
                        print(
                            f"\n[Checkpoint Violation Caught (Risk Triggered)]: Saved $20 but got caught! Operations locked for 1 turn.")
                    else:
                        state["capital"] += 20
                        print(f"\n[Checkpoint Evaded Safely]: Saved +$20 inspection fees with zero penalties incurred!")
                input("\nPress Enter to return to dashboard...")

            elif cat_choice == "2":
                print("\n MAINTENANCE ACTIONS:")
                print("   [1] Preventative System Check: Consumes -5 Raw for parts, shaves -$25 upkeep.")
                print("   [2] Equipment Recalibration: Boosts next Major Action yield/success by +5%.")
                print("   [3] Tooling Salvage: Reclaims spare parts for +5 Raw Materials.")
                print("   [4] Deferred Maintenance Sweep: Gains +$20 Capital, but risks a -$50 breakdown next turn.")
                print("   [5] Patchwork Wire Job: Fixes fault cheaply, but risks destroying 3 Finished Goods.")

                maint_act = input("Select action (1-5): ").strip()
                state["minor_actions_used"] += 1
                clear_screen()

                if maint_act == "1":
                    if state["raw_materials"] >= 5:
                        state["raw_materials"] -= 5
                        state["base_maintenance_cost"] = max(0, state["base_maintenance_cost"] - 25)
                        print(
                            "\n[Preventative Check Successful]: Shaved -$25 off monthly upkeep using 5 Raw Materials.")
                    else:
                        print("\n[Failed]: Not enough Raw Materials (need 5).")
                elif maint_act == "2":
                    state["next_major_yield_bonus"] += 0.05
                    print("\n[Equipment Recalibrated]: Next Major Action success/yield boosted by +5%.")
                elif maint_act == "3":
                    state["raw_materials"] += 5
                    print("\n[Tooling Salvage Successful]: Reclaimed +5 Raw Materials.")
                elif maint_act == "4":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 30
                        print(
                            f"\n[Deferred Breakdown (Risk Triggered)]: Gained $20 now, but equipment broke down costing -$50 total repairs!")
                    else:
                        state["capital"] += 20
                        print(
                            f"\n[Deferred Sweep Safe]: Skipped repairs cleanly and pocketed +$20 Capital with no breakdown!")
                elif maint_act == "5":
                    if evaluate_minor_action_risk(state) and state["finished_goods"] >= 3:
                        state["finished_goods"] -= 3
                        print(
                            f"\n[Wire Job Short-Circuit (Risk Triggered)]: Fixed cheap, but auxiliary surge destroyed 3 Finished Goods.")
                    else:
                        print(f"\n[Wire Job Successful]: Fixed fault cleanly with zero stock loss!")
                input("\nPress Enter to return to dashboard...")

            elif cat_choice == "3":
                print("\n MARKET ACTIONS:")
                print("   [1] Spot Market Sale: Instantly sells up to 5 Finished Goods for +$100.")
                print("   [2] Micro Future Hedge: Locks in +$15 Capital bonus on market sales this turn.")
                print("   [3] Fire-Sale Dumping: Offloads 10 goods quickly, but risks depressing market price.")
                print("   [4] Sub-Contract Freight: Pays -$20 to rush delivery, but risks losing 2 goods.")
                print("   [5] Speculative Currency Hold: Trades currency, but risks a -$25 fluctuation loss.")

                mkt_act = input("Select action (1-5): ").strip()
                state["minor_actions_used"] += 1
                clear_screen()

                if mkt_act == "1":
                    sold_qty = min(state["finished_goods"], 5)
                    if sold_qty > 0:
                        state, earned, sold = execute_sales_contract(state, sold_qty)
                        print(f"\n[Spot Sale Successful]: Sold {sold} goods instantly for ${earned:.2f}.")
                    else:
                        print("\n[Failed]: No finished goods available.")
                elif mkt_act == "2":
                    state["capital"] += 15
                    print("\n[Future Hedge Successful]: Acquired +$15 Capital hedge bonus.")
                elif mkt_act == "3":
                    if evaluate_minor_action_risk(state):
                        state["market_price_multiplier"] = max(10.0, state["market_price_multiplier"] - 5.0)
                        print(
                            f"\n[Fire-Sale Overload (Risk Triggered)]: Dumped goods, but depressed market prices to ${state['market_price_multiplier']} per unit!")
                    else:
                        sold_qty = min(state["finished_goods"], 10)
                        if sold_qty > 0:
                            state, earned, sold = execute_sales_contract(state, sold_qty)
                            print(f"\n[Fire-Sale Safe]: Offloaded {sold} goods at normal rates for ${earned:.2f}!")
                        else:
                            print("\n[Safe]: No goods to dump, hedge completed safely.")
                elif mkt_act == "4":
                    if evaluate_minor_action_risk(state) and state["finished_goods"] >= 2:
                        state["finished_goods"] -= 2
                        state["capital"] -= 20
                        print(
                            f"\n[Freight Mishap (Risk Triggered)]: Paid $20 rush fee, but handling mishandling lost 2 Finished Goods.")
                    else:
                        state["capital"] -= 20
                        print(f"\n[Freight Safe]: Paid $20 rush fee and delivered stock cleanly with zero damage!")
                elif mkt_act == "5":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 25
                        print(
                            f"\n[Currency Fluctuation Loss (Risk Triggered)]: Currency dropped, deducting -$25 Capital.")
                    else:
                        state["capital"] += 10
                        print(
                            f"\n[Currency Speculation Win]: Market swung favorably, granting +$10 Capital instead of a loss!")
                input("\nPress Enter to return to dashboard...")

            elif cat_choice == "4":
                print("\n LOGISTICS ACTIONS:")
                print("   [1] Scrap Metal Recycling: Recycles waste into +$25 Capital.")
                print("   [2] Route Optimization: Cuts shipping overhead by +$2 per sale transaction.")
                print("   [3] Emergency Cargo Express: Pays -$25 for +10 Raw, but risks transit delays.")
                print("   [4] Warehouse Overfill: Accepts extra shipment, but risks storage penalty.")
                print("   [5] Unlicensed Courier: Hires cheap transport, but risks cargo impoundment.")

                log_act = input("Select action (1-5): ").strip()
                state["minor_actions_used"] += 1
                clear_screen()

                if log_act == "1":
                    state["capital"] += 25
                    print("\n[Recycling Successful]: Recycled factory waste into +$25 Capital.")
                elif log_act == "2":
                    state["market_price_multiplier"] += 2.0
                    print("\n[Route Optimized]: Permanent transaction shipping overhead value added.")
                elif log_act == "3":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 25
                        print(
                            f"\n[Cargo Delay (Risk Triggered)]: Paid $25 premium, but shipment got stuck in customs with zero delivery.")
                    else:
                        state["raw_materials"] += 10
                        state["capital"] -= 25
                        print(f"\n[Cargo Express Safe]: Paid $25 and instantly received +10 Raw Materials!")
                elif log_act == "4":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 15
                        print(
                            f"\n[Storage Overfill Penalty (Risk Triggered)]: Overflow incurred a -$15 storage penalty.")
                    else:
                        state["raw_materials"] += 15
                        print(f"\n[Overfill Handled Cleanly]: Stored extra stock safely with zero penalty fees!")
                elif log_act == "5":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 10
                        print(f"\n[Courier Impound (Risk Triggered)]: Cheap courier intercepted; -$10 fee lost.")
                    else:
                        state["raw_materials"] += 5
                        print(f"\n[Courier Safe]: Cheap transport delivered +5 raw materials without getting caught!")
                input("\nPress Enter to return to dashboard...")

            elif cat_choice == "5":
                print("\n HUMAN CAPITAL ACTIONS:")
                print("   [1] Floor Team Commendation: Boosts next Major Action success/yield by +10%.")
                print("   [2] Apprentice Training Shift: Generates +3 Raw Materials safely.")
                print("   [3] Mandatory Overtime Push: Gains +5 Raw, but risks raising upkeep friction.")
                print("   [4] Cut Shift Break Times: Gains +$20 Capital, but risks production slowdowns.")
                print("   [5] Emergency Temp Workers: Spends -$30 to hire help, but risks ruined materials.")

                hr_act = input("Select action (1-5): ").strip()
                state["minor_actions_used"] += 1
                clear_screen()

                if hr_act == "1":
                    state["next_major_yield_bonus"] += 0.10
                    print("\n[Morale Boosted]: Next Major Action success/yield increased by +10%.")
                elif hr_act == "2":
                    state["raw_materials"] += 3
                    print("\n[Apprentice Training Successful]: Generated +3 Raw Materials.")
                elif hr_act == "3":
                    if evaluate_minor_action_risk(state):
                        state["base_maintenance_cost"] += 10
                        print(
                            f"\n[Union Friction (Risk Triggered)]: Gathered goods, but friction increased next month's upkeep by +$10.")
                    else:
                        state["raw_materials"] += 5
                        print(f"\n[Overtime Push Safe]: Harvested +5 Raw Materials with zero union friction!")
                elif hr_act == "4":
                    if evaluate_minor_action_risk(state):
                        print(
                            f"\n[Worker Fatigue (Risk Triggered)]: Gained $20 now, but fatigue caused a minor slowdown next turn.")
                    else:
                        state["capital"] += 20
                        print(
                            f"\n[Break Times Cut Safely]: Secured +$20 Capital in labor savings with zero fatigue penalties!")
                elif hr_act == "5":
                    if evaluate_minor_action_risk(state):
                        state["capital"] -= 30
                        print(
                            f"\n[Temp Worker Blunder (Risk Triggered)]: Spent $30, but untrained temp workers ruined 5 Raw Materials.")
                    else:
                        state["raw_materials"] += 10
                        state["capital"] -= 30
                        print(
                            f"\n[Temp Workers Proficient]: Spent $30 and temp staff helped secure +10 Raw Materials cleanly!")
                input("\nPress Enter to return to dashboard...")

        # Handle Sales Contract [7]
        elif choice == "7":
            if minor_exhausted:
                clear_screen()
                input("\n[!] You have no Minor Actions left this month! Press Enter to continue.")
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
        elif choice == "8" or (major_exhausted and minor_exhausted):
            clear_screen()
            print(f"=== END OF MONTH {state['current_month']} SUMMARY ===")

            cave_in = state["research_levels"]["efficiency"] >= 4 and random.random() < calculate_effective_risk(state)
            state, action_logs = process_end_of_month_rollover(state, cave_in)

            for log in action_logs:
                print(log)

            print(f"\n Advancing time cycle to Month {state['current_month']}...")
            input("\nPress Enter to begin the new month...")

            state = handle_monthly_event(state)

        elif choice == "9":
            clear_screen()
            print(f"\nExiting {state['difficulty_name']} simulation. Thanks for playing CliFactory!")
            break
        else:
            clear_screen()
            input("\n[!] Invalid choice. Press Enter to try again.")


if __name__ == "__main__":
    run_game()