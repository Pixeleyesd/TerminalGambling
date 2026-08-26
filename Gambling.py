import random
import time
race_events = random.randrange(20,35)
horses = ['Midnight Dash', 'Silver Hoof', 'Storm Rider', 'Golden Gallop', 'Thunder Bloom', 'Rose Runner', 'Wild Clover', 'Sunfire Spur', 'North Wind', 'Velvet Coast', 'Cinder Stride', 'Mossy Valley', 'Racing Belle', 'Blue Horizon', 'Night Whisper', 'Prairie Star', 'Frost Arrow', 'Iron Echo', 'Canyon Glow', 'Dawn Charge', 'Riverton Rose', 'Long Grass']
retired_horses = []
#you can use random.shuffle to make the horses go into a different order
random.shuffle(horses)

print(f"Welcome to another Horse Race!")
input("And now, for the starting lineup! [press enter to view] \n")
#cool stuff
for position, horse in enumerate(horses, start=1):
    print(f"P{position}: {horse}")
input("Press Enter to start the race! \n")
print("The race is on! The field is flying towards the first big moment! ")
print("And it's the gates open, and away we go! \n")
time.sleep(0.5)
yellow_flag = 0
red_flag = 0
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
            #Overtake code here
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
            yellow_flag = 1

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
                yellow_flag = 1

        elif event == 17:
            if spin == 1:
                horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[horse_position]} slips coming out of Turn {str(turn)}, and manages to continue.")
            elif spin == 2:
                horse_position = random.randint(1,len(horses)-1)
                print(f"{horses[horse_position]} slips coming out of Turn {str(turn)}, crashes into the fence, and is out.")
                retired_horses.append(horses[horse_position])
                horses.remove(horses[horse_position])  
                yellow_flag = 1
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
                yellow_flag = 1

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
            penalty = random.randrange (1,3)
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
#new stuff
print(f"{horses[0]} wins the Horse Race!")
time.sleep(0.5)
for position, horse in enumerate(horses, start=1):
    print(f"P{position}: {horse}")
    time.sleep(0.2)

if not retired_horses:
    pass
else:
    print("Retired:")
    for position, horse in enumerate(retired_horses, start=1):
        print(f"{horse}")
        time.sleep(0.2)