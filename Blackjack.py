import random
import time
import keyboard
import os
import sys

if os.name == "nt": 
    import msvcrt
else:
    import select

def clear_input_buffer():
    if os.name == "nt":
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()

def wait_for_key_release():
    while (
        keyboard.is_pressed("up")
        or keyboard.is_pressed("down")
        or keyboard.is_pressed("enter")
    ):
        time.sleep(0.05)

def read_menu_key():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name

def draw_menu(title, options, player_balance, selected_index):
    print("\033c", end="")
    print("\n" + "="*30)
    print(f"--- {title} ---")
    print(f"Current Balance: ${player_balance}")
    print("="*30)
    print("Use UP and DOWN arrows to select, and ENTER to choose.\n")

    for i, option in enumerate(options):
        if i == selected_index:
            print(f"\033[7m  {option}  \033[0m")
        else:
            print(f"  {option}  ")

def get_menu_selection(title, options, player_balance):
    selected_index = 0
    clear_input_buffer()
    while True:
        draw_menu(title, options, player_balance, selected_index)
        key = read_menu_key()

        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key == "enter":
            return selected_index

def instructions_menu():
    print("\033c", end="")
    print("\n" + "="*30)
    print("--- BLACKJACK INSTRUCTIONS ---")
    print("="*30)
    print("\nHow to Play:")
    print("Your goal is to get your card total as close to 21")
    print("as possible without going over (busting).")
    print("")
    print("Card Values:")
    print("- Number cards are worth their face value.")
    print("- Face cards (Jack, Queen, King) are worth 10.")
    print("- Aces are worth 1 or 11 (whichever benefits you more).")
    print("")
    print("Actions:")
    print("- Hit: Draw another card.")
    print("- Stand: Keep your current hand and end your turn.")
    print("")
    print("The dealer must continue to hit until their total")
    print("is 17 or higher. Beating the dealer pays 2x your bet.")
    print("")

    time.sleep(0.05)  # Wait for key release to prevent skipping menus
    
    wait_for_key_release()
    clear_input_buffer()
    input("[press enter to return to blackjack menu]")
    clear_input_buffer()
    print("\033c", end="")

    time.sleep(0.05)  # Wait for key release to prevent skipping menus

def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            score += 10
        elif card == 'A':
            aces += 1
            score += 11
        else:
            score += card
    
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
        
    return score

def play_blackjack(player_balance):
    clear_input_buffer()
    
    # Blackjack Main Menu
    while True:
        main_options = ["Play a Hand", "Instructions", "Back"]
        main_index = get_menu_selection("BLACKJACK", main_options, player_balance)
        
        if main_index == 0:
            break
        elif main_index == 1:
            instructions_menu()
        elif main_index == 2:
            print("\033c", end="")
            wait_for_key_release()
            return player_balance
            
    # Enter Bet Amount
    print("\033c", end="")
    while True:
        time.sleep(0.05)  # Wait for key release to prevent skipping menus
        clear_input_buffer()
        try:
            bet_amount = int(input(f"Enter your bet amount (Max ${player_balance}): $"))
            if 0 < bet_amount <= player_balance:
                break
            else:
                print("Invalid amount. Please bet a positive number within your balance.")
        except ValueError:
            print("Please enter a valid number.")

    # Deck setup
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    # Player's Turn
    while True:
        player_score = calculate_score(player_hand)
        
        print("\033c", end="")
        print(f"--- BLACKJACK ---")
        print(f"Bet: ${bet_amount}")
        print(f"\nDealer's Hand:")
        print(f"[{dealer_hand[0]}] [?]")
        
        print(f"\nYour Hand: {player_hand} (Score: {player_score})")
        
        if player_score == 21:
            print("\nBlackjack!")
            input("[press enter to continue]")
            break
        elif player_score > 21:
            print("\nBust!")
            input("[press enter to continue]")
            break
            
        options = ["Hit", "Stand"]
        wait_for_key_release()
        choice = get_menu_selection("YOUR MOVE", options, player_balance)
        
        if choice == 0:
            player_hand.append(deck.pop())
        elif choice == 1:
            break
            
    # Dealer's turn
    player_score = calculate_score(player_hand)
    
    if player_score <= 21:
        print("\033c", end="")
        print(f"--- DEALER's TURN ---")
        dealer_score = calculate_score(dealer_hand)
        print(f"Dealer reveals hand: {dealer_hand} (Score: {dealer_score})")
        input("[press enter to continue]")
        
        while dealer_score < 17:
            dealer_hand.append(deck.pop())
            dealer_score = calculate_score(dealer_hand)
            print(f"Dealer hits: {dealer_hand[-1]}")
            print(f"Dealer hand: {dealer_hand} (Score: {dealer_score})")
            input("[press enter to continue]")
            
    # Evaluate outcome
    print("\n--- RESULTS ---")
    dealer_score = calculate_score(dealer_hand)
    
    if player_score > 21:
        print(f"You busted. You lost ${bet_amount}.")
        player_balance -= bet_amount
    elif dealer_score > 21:
        print(f"Dealer busted! You won ${bet_amount}!")
        player_balance += bet_amount
    elif player_score > dealer_score:
        print(f"You beat the dealer! You won ${bet_amount}!")
        player_balance += bet_amount
    elif dealer_score > player_score:
        print(f"Dealer wins. You lost ${bet_amount}.")
        player_balance -= bet_amount
    else:
        print("Push! It's a tie, your bet is returned.")

    wait_for_key_release()
    clear_input_buffer()
    input("\n[press enter to return to menu]")
    clear_input_buffer()
    print("\033c", end="")
    wait_for_key_release()

    return player_balance