import random
from scraper import playerweight
from num2words import num2words
import re

player_n = 0
players = {}
usernames = {}

choose = input("Do you want to get player weights from tracker.gg, or input them manually? (T for tracker.gg, M for manually): ").lower()

if choose == "t":

    #'''
    while len(usernames) < 10:
        player_n += 1
        position = num2words(player_n, ordinal=True)
        userin = input(f"{position} player's username (no spaces between username and tag): ")
        splitted = re.split(r'#', userin)
        #print(splitted)
        riottag = splitted[-1]
        splitted.remove(riottag)
        #print(splitted)
        riotname = str(*splitted)
        #print(f"tag:{riottag}, name:{riotname}")
        usernames[riotname] = riottag

    print(usernames)

    for i in usernames:
        uname = i
        utag = usernames[i]
        username, weight = playerweight(uname, utag)
        players[username] = weight
        print(f"List so far: {players}")

    print(players)
    #'''


elif choose == "m":
        while len(players) < 10:
            player_n += 1
            position = num2words(player_n, ordinal=True)
            userin = input(f"{position} player's name & score. Separate with comma (ex: 'SEN curry, 0.743): ")
            splitted = re.split(r', ', userin)

            scorestr = splitted[-1]
            score = float(splitted[-1])
            splitted.remove(scorestr)

            name = str(*splitted)
            #print(f"tag:{riottag}, name:{riotname}")
            players[name] = score

        print(players)


while True:
    try:
        debuff = input("Do you want to change any weights? (yes/no): ").lower()

        if debuff == "yes":
            debuff = input("example: 'nerf ranchbleam: 0.2'. this will subract 0.2 from ranchbleam. saying 'buff' will add instead.): ")
            if "nerf" in debuff:
                splitted = re.split(r'nerf ', debuff)
                #print(f"splitted = {splitted}")
                playername = splitted[1]
                #print(f"playername = {playername}")
                splitted2 = re.split(r': ', playername)
                #print(f"splitted2 = {splitted2}")
                debuffvalue = float(splitted2[1])
                print(f"nerf = {debuffvalue}")
                playername = splitted2[0]
                print(f"player = {playername}")
                value = float(players[playername])

                if 0 < value - debuffvalue < 1:
                    players[playername] = value - debuffvalue
                elif value - debuffvalue >= 1:
                    players[playername] = 1
                elif value - debuffvalue <= 0:
                    players[playername] = 0
                
                print(players)
                again = input("Do you want to modify another player? (yes/no): ").lower()
                if again == "yes":
                    pass
                if again == "no":
                    break
                
            if "buff" in debuff:
                splitted = re.split(r'buff ', debuff)
                #print(f"splitted = {splitted}")
                playername = splitted[1]
                #print(f"playername = {playername}")
                splitted2 = re.split(r': ', playername)
                #print(f"splitted2 = {splitted2}")
                debuffvalue = float(splitted2[1])
                print(f"buff = {debuffvalue}")
                playername = splitted2[0]
                print(f"player = {playername}")
                value = float(players[playername])

                if 0 < value + debuffvalue < 1:
                    players[playername] = value + debuffvalue
                elif value + debuffvalue >= 1:
                    players[playername] = 1
                elif value + debuffvalue <= 0:
                    players[playername] = 0

                print(players)
                again = input("Do you want to modify another player? (yes/no): ").lower()
                if again == "yes":
                    pass
                if again == "no":
                    break
            else:
                pass
        else:
            break
    except Exception as e:
        print(f"Invalid input, {e}")

print(players)

def teamcreator(players):
    player_names = list(players.keys())
    random.shuffle(player_names)

    sorted_players = sorted(player_names, key=lambda x: players[x], reverse=True)

    team1 = []
    team2 = []
    team1_value = 0
    team2_value = 0

    for player in sorted_players:
        if team1_value <= team2_value:
            team1.append(player)
            team1_value += players[player]
        else:
            team2.append(player)
            team2_value += players[player]

    return team1, team2, team1_value, team2_value

team1, team2, team1_value, team2_value = teamcreator(players)

print()
print("############## TEAMS ##############")
print()
print("Team 1:")
for player in team1:
    print(player, "-", players[player])
print("Team 1 Total Value:", team1_value)

print("\nTeam 2:")
for player in team2:
    print(player, "-", players[player])
print("Team 2 Total Value:", team2_value)
