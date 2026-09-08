
import os
import random


def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')


def select_difficulty():
  while True:
    clear_screen()
    print('=' * 75)
    print('          🏭 CLIFACTORY: SELECT CORPORATE TIER 🏭          ')
    print('=' * 75)
    print('   [1] SUBSIDIZED STARTUP (Easy)')
    print('       - Starting Capital: $800.00')
    print('       - Guaranteed Positive Outcomes: First 4 Months')
    print('\n   [2] MID-MARKET (Normal)')
    print('       - Starting Capital: $500.00')
    print('       - Guaranteed Positive Outcomes: First 2 Months')
    print('\n   [3] HOSTILE TAKEOVER (Hard)')
    print('       - Starting Capital: $250.00')
    print('       - Guaranteed Positive Outcomes: None (Pure RNG)')
    print('-' * 75)

    choice = input('Select tier (1-3): ').strip()

    if choice == '1':
      return 'Subsidized Startup', 800.0, 4
    elif choice == '2':
      return 'Mid-Market', 500.0, 2
    elif choice == '3':
      return 'Hostile Takeover', 250.0, 0
    else:
      input('\n[!] Invalid choice. Press Enter to try again.')


def run_game():
  diff_name, capital, guaranteed_months = select_difficulty()

  # Game State Variables
  current_month = 1
  raw_materials = 20  # Starting baseline buffer
  finished_goods = 0

  # Passive Production Parameters (Mining > Refining)
  base_passive_mining = 25  # Raw materials extracted per month
  base_passive_refining = 18  # Raw materials converted to finished goods per month

  # Factory Infrastructure State Variables
  factory_expansion_levels = 0
  base_maintenance_cost = 50
  futures_contract_active = False
  skip_next_major = False

  # R&D Unlocked Tech Flags & Modifiers
  unlocked_techs = {
      "logistics": False,
      "efficiency": False,
      "safety": False,
      "marketing": False,
  }
  market_price_multiplier = 20.0  # Base price per unit

  # Turn tracking constraints
  major_action_taken = False
  max_minor_actions = 2
  minor_actions_used = 0

  while True:
    # --- CHECK LOSS CONDITION (Bankruptcy) ---
    if capital <= 0:
      clear_screen()
      print('=' * 75)
      print('                     💀 GAME OVER: BANKRUPTCY 💀                     ')
      print('=' * 75)
      print(f' Month Reached: {current_month}')
      print(
          ' Capital reserves have hit $0. Your corporate board has voted to'
          ' liquidate'
      )
      print(
          ' assets, and your company has been acquired in a hostile buyout.'
          ' You'
      )
      print(' are officially no longer the CEO.')
      print('=' * 75)
      input('\nPress Enter to exit CliFactory...')
      break

    # --- CHECK VICTORY CONDITION (Monopoly) ---
    total_output_rate = base_passive_refining + (
        factory_expansion_levels * 15
    )
    if capital >= 10000.0 and total_output_rate >= 100:
      clear_screen()
      print('=' * 75)
      print('                   👑 VICTORY: GLOBAL MONOPOLY 👑                    ')
      print('=' * 75)
      print(f' Month Reached: {current_month}')
      print(f' Final Capital: ${capital:.2f}')
      print(f' Monthly Production Output: {total_output_rate} goods/mo')
      print(
          ' Extraordinary work! You have completely crushed all market'
          ' competition,'
      )
      print(
          ' achieved absolute supply-chain dominance, and established a'
          ' global monopoly.'
      )
      print('=' * 75)
      input('\nPress Enter to exit CliFactory...')
      break

    clear_screen()

    # --- TOP HEADER ---
    header_left = f'🏭 CLIFACTORY [{diff_name.upper()}]'
    header_right = f'📅 MONTH: {current_month}'
    print('=' * 75)
    print(f'{header_left:<45}{header_right:>28}')
    print('=' * 75)

    # --- STATUS PANEL ---
    print(
        f' Capital: ${capital:.2f}  |  Raw Materials: {raw_materials}'
        f'  |  Finished Goods: {finished_goods}'
    )
    print(
        f' Upkeep: ${base_maintenance_cost}/mo  |  Mining: {base_passive_mining}'
        f' Raw/mo  |  Refining: {base_passive_refining} Goods/mo'
    )

    active_tech_list = [
        k.capitalize() for k, v in unlocked_techs.items() if v
    ]
    tech_display = (
        ', '.join(active_tech_list) if active_tech_list else 'None'
    )
    print(f' Unlocked R&D Fields: [{tech_display}]')

    if current_month <= guaranteed_months:
      print(
          ' Status: 🛡️ Guaranteed Positive Outcome Active'
          f' ({guaranteed_months - current_month + 1} months left)'
      )
    else:
      print(' Status: ⚠️ Standard Market Risk Active')

    if skip_next_major:
      print(' Status Alert: 🔴 Major Action locked due to prior failure!')

    print(
        f' Actions Left this Month -> Major: '
        f"{'0 (Done/Locked)' if (major_action_taken or skip_next_major) else '1 Available'}"
        f' | Minor: {max_minor_actions - minor_actions_used}/{max_minor_actions}'
    )
    print('-' * 75)

    # --- MENU INTERFACE ---
    print(' CHOOSE YOUR ACTIONS:')
    print('\n [MAJOR ACTIONS (Max 1 per month)]')
    if not major_action_taken and not skip_next_major:
      print('   [1] Prospect Unknown Sector (Exploration: +75 Raw / -$100 Fine)')
      print(
          '   [2] Construct Factory Expansion (Expansion: -$300 Cap, boosts'
          ' output)'
      )
      print('   [3] Invest in R&D (Research one of 4 specialized fields)')
      print(
          '   [4] Corporate Futures Contract (Market: +50% Sale Price or -$100'
          ' Penalty)'
      )
      print(
          '   [5] Bulk Material Import (Supply Chain: Instant +150 Raw for'
          ' $150)'
      )
    else:
      print('   [1-5] (Major Action unavailable or completed this month)')

    print('\n [MINOR ACTIONS (Limited per month)]')
    print('   [6] Secure Sales Contract & Sell Finished Goods on Market')
    print('   [7] Oversee operations & adjust logistics workflows')

    print('\n [SYSTEM CONTROLS]')
    print('   [8] End Month Early & Proceed to Next Cycle')
    print('   [9] Quit Game')
    print('-' * 75)

    choice = input('Select an option (1-9): ').strip()

    # --- ACTION HANDLERS ---
    if choice in ['1', '2', '3', '4', '5']:
      if major_action_taken or skip_next_major:
        clear_screen()
        if skip_next_major:
          print(
              '\n[!] Major Action is locked this month due to prior failure!'
          )
        else:
          print(
              '\n[!] You have already performed your Major Action this'
              ' month!'
          )
        input('Press Enter to continue.')
        continue

      major_action_taken = True
      clear_screen()

      # 1. Prospect Unknown Sector
      if choice == '1':
        print(f'--- MONTH {current_month}: PROSPECT UNKNOWN SECTOR ---')
        if current_month <= guaranteed_months:
          outcome = 'reward'
        else:
          outcome = random.choice(['reward', 'hazard'])

        if outcome == 'reward':
          raw_materials += 75
          print(
              '\n Success! Located high-yield rare mineral deposit. (+75 Raw'
              ' Materials)'
          )
        else:
          capital -= 100
          print(
              '\n Disaster! Environmental breach triggered a hazard fine. (-$100'
              ' Capital)'
          )

      # 2. Construct Factory Expansion
      elif choice == '2':
        print(f'--- MONTH {current_month}: CONSTRUCT FACTORY EXPANSION ---')
        if capital >= 300:
          capital -= 300
          factory_expansion_levels += 1
          base_maintenance_cost += 25
          print(
              '\n Construction successful! Deducted $300 Capital. Factory'
              ' expanded (Base refining rate boosted, maintenance cost increased'
              ' by +$25/mo).'
          )
        else:
          print('\n[!] Insufficient Capital! Construction requires $300.')
          major_action_taken = False

      # 3. Invest in R&D
      elif choice == '3':
        print(f'--- MONTH {current_month}: RESEARCH & DEVELOPMENT ---')
        print(
            'Select a research field to invest in (-$100 Research Funding):'
        )
        print('  [1] Logistics (Supply chain optimization & transport)')
        print('  [2] Efficiency (Refining and production yield upgrades)')
        print('  [3] Safety (Risk mitigation and hazard reduction)')
        print('  [4] Marketing & Finance (Brand equity and sales optimization)')
        print('  [5] Cancel R&D Investment')

        rd_choice = input('\nSelect field (1-5): ').strip()

        if rd_choice in ['1', '2', '3', '4']:
          if capital >= 100:
            capital -= 100
            fail_chance = (
                0.0 if current_month <= guaranteed_months else 0.05
            )
            if random.random() < fail_chance:
              print(
                  '\n[!] RESEARCH FAILURE! The laboratory encountered an'
                  ' unrecoverable experimental dead-end. -$100 funds wasted with'
                  ' no technology unlocked.'
              )
            else:
              if rd_choice == '1':
                unlocked_techs['logistics'] = True
                base_maintenance_cost = max(
                    10, base_maintenance_cost - 20
                )
                print(
                    '\n Success! Unlocked Advanced Logistics. Base'
                    ' infrastructure maintenance permanently reduced by -$20/mo!'
                )
              elif rd_choice == '2':
                unlocked_techs['efficiency'] = True
                print(
                    '\n Success! Unlocked Lean Efficiency. Passive refining'
                    ' yield bonus activated.'
                )
              elif rd_choice == '3':
                unlocked_techs['safety'] = True
                print(
                    '\n Success! Unlocked Automated Safety Protocols. Hazard'
                    ' fines and risks are now completely neutralized.'
                )
              elif rd_choice == '4':
                unlocked_techs['marketing'] = True
                market_price_multiplier += 10.0
                print(
                    '\n Success! Unlocked Global Brand Equity. Base market value'
                    ' for finished goods permanently increased to $'
                    f'{market_price_multiplier:.1f} per unit!'
                )
          else:
            print('\n[!] Insufficient Capital! R&D investment requires $100.')
            major_action_taken = False
        else:
          print('\n[!] R&D action canceled. Major action refunded.')
          major_action_taken = False

      # 4. Corporate Futures Contract
      elif choice == '4':
        print(f'--- MONTH {current_month}: CORPORATE FUTURES CONTRACT ---')
        futures_contract_active = True
        print(
            '\n Secured corporate futures contract! All finished goods sold this'
            ' month enjoy a +50% price multiplier. (Warning: Must complete'
            ' sales contract or face a -$100 penalty at month end).'
        )

      # 5. Bulk Material Import
      elif choice == '5':
        print(f'--- MONTH {current_month}: BULK MATERIAL IMPORT ---')
        if capital >= 150:
          capital -= 150
          if current_month <= guaranteed_months or unlocked_techs['safety']:
            loss_roll = False
          else:
            loss_roll = random.random() < 0.25

          if not loss_roll:
            raw_materials += 150
            print(
                '\n Bulk import successful! Instant influx of +150 Raw'
                ' Materials.'
            )
          else:
            print(
                '\n CARGO THEFT/LOSS! Transport shipment intercepted. -$150'
                ' Capital lost with zero materials delivered.'
            )
        else:
          print('\n[!] Insufficient Capital! Bulk import requires $150.')
          major_action_taken = False

      input('\nPress Enter to return to the dashboard...')

    # Minor Actions & Controls
    elif choice == '6':
      if minor_actions_used >= max_minor_actions:
        clear_screen()
        input(
            '\n[!] You have no Minor Actions left this month! Press Enter to'
            ' continue.'
        )
        continue
      minor_actions_used += 1
      clear_screen()
      print(f'--- MONTH {current_month}: SALES CONTRACT EXECUTION ---')

      current_unit_price = market_price_multiplier
      if futures_contract_active:
        current_unit_price *= 1.5
        print(' [Active Contract]: +50% price multiplier applied.')

      if finished_goods > 0:
        earned = finished_goods * current_unit_price
        capital += earned
        print(
            f'\n Successfully secured sales contract! Sold {finished_goods}'
            f' units of finished goods for ${earned:.2f}.'
        )
        finished_goods = 0
        futures_contract_active = False
      else:
        print(
            '\n[!] No finished goods available in inventory to fulfill a sales'
            ' contract.'
        )
      input('\nPress Enter to return to the dashboard...')

    elif choice == '7':
      if minor_actions_used >= max_minor_actions:
        clear_screen()
        input(
            '\n[!] You have no Minor Actions left this month! Press Enter to'
            ' continue.'
        )
        continue
      minor_actions_used += 1
      clear_screen()
      print(f'--- MONTH {current_month}: OPERATIONS AUDIT ---')
      capital += 50
      print(
          '\n Routine infrastructure audit completed. Optimized supply lines'
          ' recovered $50 in overhead savings.'
      )
      input('\nPress Enter to return to the dashboard...')

    elif choice == '8' or (
        (major_action_taken or skip_next_major)
        and minor_actions_used >= max_minor_actions
    ):
      clear_screen()
      print(f'=== END OF MONTH {current_month} SUMMARY ===')

      if futures_contract_active:
        capital -= 100
        print(
            ' [Penalty]: Corporate futures contract sales quota missed! Incurred'
            ' -$100 penalty.'
        )
        futures_contract_active = False

      # --- PASSIVE MINING & REFINING CYCLE ---
      # Mining quantity is higher than refining quantity to maintain buffer surplus
      total_mined = base_passive_mining + (
          factory_expansion_levels * 5
      )  # Extra mining per expansion
      raw_materials += total_mined
      print(
          f' Autonomous extraction systems mined +{total_mined} raw materials.'
      )

      total_refined_capacity = base_passive_refining + (
          factory_expansion_levels * 15
      )
      if unlocked_techs['efficiency']:
        total_refined_capacity = int(total_refined_capacity * 1.3)  # +30% boost

      # Refine only as many as raw materials permit
      actual_refined = min(raw_materials, total_refined_capacity)
      raw_materials -= actual_refined
      finished_goods += actual_refined
      print(
          f' Factory converted {actual_refined} raw materials into finished'
          ' sellable goods.'
      )

      # Deduct monthly maintenance
      capital -= base_maintenance_cost
      print(
          f' Deducted ${base_maintenance_cost} monthly base infrastructure'
          ' maintenance cost.'
      )

      print(f'\n Advancing time cycle to Month {current_month + 1}...\n')

      current_month += 1
      major_action_taken = False
      skip_next_major = False
      minor_actions_used = 0

      input('\nPress Enter to begin the new month...')

    elif choice == '9':
      clear_screen()
      print(
          f'\nExiting {diff_name} simulation. Thanks for playing CliFactory!'
      )
      break
    else:
      clear_screen()
      input('\n[!] Invalid choice. Press Enter to try again.')


if __name__ == '__main__':
  run_game()