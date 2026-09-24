import random
import time
import keyboard
import os
import sys

if os.name == "nt": #yoinked from stackoverflow so itworks for linux and windows
    import msvcrt
else:
    import select


def clear_input_buffer(): #yoinked from stackoverflow (i think this is for linux and windows compatibility too...?)
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
        time.sleep(0.05) #you need these time.sleeps to prevent the program from skipping menus, otherwise it will skip the menu if you hold down a key for too long


def read_menu_key():
    while True:
        event = keyboard.read_event(suppress=True) #this makes it so the keypresses don't queue for the text input that comes afrer

        if event.event_type == keyboard.KEY_DOWN:
            return event.name


def instructions_menu():
    print("\033c", end="")
    print("\n" + "="*30)
    print("--- HORSE RACE INSTRUCTIONS ---")
    print("="*30)
    print("\nHow to Play:")
    print("Choose one of the five available horses and enter")
    print("the amount you want to bet.")
    print("")
    print("Each horse has a different chance of winning.")
    print("Horses with higher chances have lower payouts,")
    print("while horses with lower chances have higher payouts.")
    print("")
    print("Your horse earns its payout if it finishes in")
    print("1st, 2nd, or 3rd place.")
    print("")
    print("If your horse finishes outside the podium,")
    print("the bet is lost.")
    print("")
    print("The race contains random events such as overtakes,")
    print("penalties, pit stops, and horses being retired.")
    print("")
    input("[press enter to return to race menu]")
    clear_input_buffer()
    print("\033c", end="")


def play_horse_race(player_balance):
    clear_input_buffer()

    options = ["Start Race", "Instructions", "Back"]
    selected_index = 0

    while True:
        print("\033c", end="")
        print("\n" + "="*30)
        print("--- RACE MENU ---")
        print(f"Current Balance: ${player_balance}")
        print("="*30)
        print("Use UP and DOWN arrows to select, and ENTER to choose.\n")

        # Print menu with highlights
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"\033[7m  {option}  \033[0m")
            else:
                print(f"  {option}  ")

        key = read_menu_key()

        if key == "up":
            selected_index = (selected_index - 1) % len(options)

        elif key == "down":
            selected_index = (selected_index + 1) % len(options)

        elif key == "enter":
            if selected_index == 0:
                break

            elif selected_index == 1:
                instructions_menu()
                selected_index = 1

            elif selected_index == 2:
                print("\033c", end="")
                return player_balance

    print("\033c", end="")
    clear_input_buffer()

    # bet loop
    while True:
        clear_input_buffer()

        try:
            bet_amount = int(input(f"Enter your bet amount (Max ${player_balance}): $"))

            if 0 < bet_amount <= player_balance:
                clear_input_buffer()
                break
            else:
                print("Invalid amount. Please bet a positive number within your balance.")
        except ValueError:
            print("Please enter a valid number.")

    # horse setup
    race_events = random.randrange(20, 35)
    horses = [
        'Midnight Dash', 'Silver Hoof', 'Storm Rider', 'Golden Gallop', 
        'Thunder Bloom', 'Rose Runner', 'Wild Clover', 'Sunfire Spur', 
        'North Wind', 'Velvet Coast', 'Cinder Stride', 'Mossy Valley', 
        'Racing Belle', 'Blue Horizon', 'Night Whisper', 'Prairie Star', 
        'Frost Arrow', 'Iron Echo', 'Canyon Glow', 'Dawn Charge', 
        'Riverton Rose', 'Long Grass'
    ]
    retired_horses = []
    random.shuffle(horses)

    race_probabilities = [ #this was made from stackoverflow code with the help of w3 schools to fix the fact that this code was sooo messy before
        17.5, 13.0, 10.0, 8.0, 7.0, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5,
        3.0, 2.5, 2.2, 1.9, 1.6, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3
    ]

    horse_probabilities = {
        horse: probability
        for horse, probability in zip(horses, race_probabilities)
    }

    payout_multipliers = {
        horse: max(2, round(100 / probability))
        for horse, probability in horse_probabilities.items()
    }

    # selecting a horse
    print("\n--- Available Horses to Bet On ---")
    for i in range(5):
        horse = horses[i]
        print(
            f"{i+1}: {horse} - "
            f"{horse_probabilities[horse]:g}% chance - "
            f"{payout_multipliers[horse]}x payout"
        )

    clear_input_buffer()

    while True:
        try:
            horse_choice = int(input("Pick a horse to bet on (1-5): "))

            if 1 <= horse_choice <= 5:
                player_horse = horses[horse_choice - 1]
                print(
                    f"\nYou placed ${bet_amount} on {player_horse} "
                    f"({horse_probabilities[player_horse]:g}% chance, "
                    f"{payout_multipliers[player_horse]}x payout)!"
                )
                clear_input_buffer()
                break
            else:
                print("Please select a valid horse number.")
        except ValueError:
            print("Please enter a valid number.")

        clear_input_buffer()

    # starting the race
    print("\nWelcome to another Horse Race!")
    clear_input_buffer()
    input("And now, for the starting lineup! [press enter to view]\n")
    clear_input_buffer()

    for position, horse in enumerate(horses, start=1):
        if horse == player_horse:
            print(f"P{position}: {horse} <--- YOUR HORSE")
        else:
            print(f"P{position}: {horse}")

    clear_input_buffer()
    input("\nPress Enter to start the race!\n")
    clear_input_buffer()

    print("The race is on! The field is flying towards the first big moment!")
    print("And it's the gates open, and away we go!\n")
    time.sleep(0.5)

    # rece event logic
    for i in range(race_events):
        event = random.randrange(1,22)
        turn = random.randrange(1,20)
        overtake_issue = random.randrange(1,5)
        horse_issue = random.randrange(1,2)
        spin = random.randrange(1,4)
        tire = random.randrange(1,3)

        try:
            if event == 1:
                overtaking_horse_position = random.randint(1,len(horses)-1)
                print(f"This should be very close into Turn {str(turn)},")
                print(f"{horses[overtaking_horse_position]} on the inside, they go shoulder to shoulder,")
                time.sleep(1)
                print(f"{horses[overtaking_horse_position]} slips wide, comes back again, and off goes {horses[overtaking_horse_position-1]},")
                time.sleep(0.5)
                print(f"THROUGH GOES {horses[overtaking_horse_position+1].upper()}! UNBELIEVABLE STUFF!")
                horses[overtaking_horse_position + 1], horses[overtaking_horse_position] = horses[overtaking_horse_position], horses[overtaking_horse_position + 1]
                horses[overtaking_horse_position], horses[overtaking_horse_position -1] = horses[overtaking_horse_position -1], horses[overtaking_horse_position]

            elif event == 2:
                overtaking_horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[overtaking_horse_position +1]} manages a DOUBLE OVERTAKE on {horses[overtaking_horse_position]} and {horses[overtaking_horse_position-1]} into Turn {str(turn)} and {str(turn+1)}!")
                horses[overtaking_horse_position + 1], horses[overtaking_horse_position] = horses[overtaking_horse_position], horses[overtaking_horse_position + 1]
                horses[overtaking_horse_position], horses[overtaking_horse_position -1] = horses[overtaking_horse_position -1], horses[overtaking_horse_position]

            elif event <= 8:
                overtaking_horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[overtaking_horse_position]} goes through the inside of {horses[overtaking_horse_position-1]} into Turn {str(turn)}!")
                horses[overtaking_horse_position], horses[overtaking_horse_position - 1] = horses[overtaking_horse_position - 1], horses[overtaking_horse_position]

            elif event <= 14:
                overtaking_horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[overtaking_horse_position]} goes through the outside of {horses[overtaking_horse_position-1]} into Turn {str(turn)}!")
                horses[overtaking_horse_position], horses[overtaking_horse_position - 1] = horses[overtaking_horse_position - 1], horses[overtaking_horse_position]

            elif event == 15:
                if overtake_issue == 1:
                    overtaking_horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[overtaking_horse_position]} tries to overtake {horses[overtaking_horse_position-1]} into Turn {str(turn)}, crashes into each other, and they are BOTH out!")
                    retired_horses.append(horses[overtaking_horse_position])
                    horses.remove(horses[overtaking_horse_position])
                    retired_horses.append(horses[overtaking_horse_position - 1])
                    horses.remove(horses[overtaking_horse_position-1])

                elif overtake_issue <= 3:
                    overtaking_horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[overtaking_horse_position]} tries to overtake {horses[overtaking_horse_position-1]} into Turn {str(turn)}, makes contact, and {horses[overtaking_horse_position]} is out!")
                    retired_horses.append(horses[overtaking_horse_position])
                    horses.remove(horses[overtaking_horse_position])

                elif overtake_issue <= 5:
                    overtaking_horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[overtaking_horse_position]} tries to overtake {horses[overtaking_horse_position-1]} into Turn {str(turn)}, makes contact, and {horses[overtaking_horse_position-1]} is out!")
                    retired_horses.append(horses[overtaking_horse_position-1])
                    horses.remove(horses[overtaking_horse_position-1])

            elif event == 16:
                if horse_issue == 1:
                    horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[horse_position]}'s saddle has issues, and the jockey boxes to retire the horse.")
                    retired_horses.append(horses[horse_position])
                    horses.remove(horses[horse_position])

                elif horse_issue == 2:
                    horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[horse_position]} is stuck in the mud, and is unable to continue.")
                    retired_horses.append(horses[horse_position])
                    horses.remove(horses[horse_position])

            elif event == 17:
                if spin == 1:
                    horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[horse_position]} slips coming out of Turn {str(turn)}, and manages to continue.")

                elif spin == 2:
                    horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[horse_position]} slips coming out of Turn {str(turn)}, crashes into the fence, and is out.")
                    retired_horses.append(horses[horse_position])
                    horses.remove(horses[horse_position])

                elif spin == 3:
                    overtaking_horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[overtaking_horse_position]} has a bad step coming out of Turn {str(turn)}, and loses position.")
                    horses.insert(overtaking_horse_position+2, horses[overtaking_horse_position])
                    horses.remove(horses[overtaking_horse_position])

                elif spin == 4:
                    overtaking_horse_position = random.randint(1,len(horses)-1)
                    print(f"{horses[overtaking_horse_position]} slips coming out of Turn {str(turn)}, crashes into {horses[overtaking_horse_position+1]}, and they are BOTH out!")
                    retired_horses.append(horses[overtaking_horse_position])
                    horses.remove(horses[overtaking_horse_position])
                    retired_horses.append(horses[overtaking_horse_position + 1])
                    horses.remove(horses[overtaking_horse_position + 1])

            elif event <= 20:
                if tire == 1:
                    compound = "Soft"
                elif tire == 2:
                    compound = "Medium"
                elif tire == 3:
                    compound = "Hard"

                horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[horse_position]} comes into the stables for {compound} tack!")
                horses.insert(horse_position + 3, horses[horse_position])
                horses.remove(horses[horse_position])

            elif event <= 22:
                penalty = random.randrange(1,3)
                horse_position = random.randint(1,len(horses)-1)

                if penalty == 1:
                    print(f"{horses[horse_position]} receives a 5-Second penalty.")
                    horses.insert(horse_position + 1, horses[horse_position])
                    horses.remove(horses[horse_position])

                if penalty == 2:
                    print(f"{horses[horse_position]} receives a 10-Second penalty.")
                    horses.insert(horse_position + 3, horses[horse_position])
                    horses.remove(horses[horse_position])

                if penalty == 3:
                    print(f"{horses[horse_position]} receives a Jockey's Drive-through penalty.")
                    horses.insert(horse_position + 5, horses[horse_position])
                    horses.remove(horses[horse_position])

        except IndexError:
            pass

        time.sleep(1)
        print("")

    # applying horse probabilities
    remaining_horses = horses[:]
    horses = []

    while remaining_horses:
        weights = [horse_probabilities[horse] for horse in remaining_horses]

        selected_horse = random.choices(
            remaining_horses,
            weights=weights,
            k=1
        )[0]

        horses.append(selected_horse)
        remaining_horses.remove(selected_horse)

    # results after the race
    winning_horse = horses[0]
    print(f"\n{winning_horse} wins the Horse Race!")

    clear_input_buffer()
    input("[press enter to view final standings]")
    clear_input_buffer()

    print("\n--- FINAL STANDINGS ---")
    for position, horse in enumerate(horses, start=1):
        if horse == player_horse:
            print(f"P{position}: {horse} <--- YOUR HORSE")
        else:
            print(f"P{position}: {horse}")

    if retired_horses:
        print("\nRetired:")
        for horse in retired_horses:
            print(f"- {horse}")

    # win/lose payout
    player_position = None

    if player_horse in horses:
        player_position = horses.index(player_horse) + 1

    if player_position is not None and player_position <= 3:
        winnings = bet_amount * payout_multipliers[player_horse]
        player_balance += winnings
        print(
            f"\nCongratulations! Your horse finished in P{player_position} "
            f"and earned ${winnings}!"
        )
    else:
        player_balance -= bet_amount
        print(
            f"\nOh no! Your horse didn't finish on the podium. "
            f"You lost your ${bet_amount} bet."
        )

    clear_input_buffer()
    input("\n[press enter to return to menu]")
    clear_input_buffer()
    print("\033c", end="")

    return player_balance