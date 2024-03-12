import concurrent.futures
from scraper import playerweight
from num2words import num2words
import re
import random

def get_player_weights(usernames):
    players = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        player_futures = {executor.submit(playerweight, uname, utag): (uname, utag) for uname, utag in usernames.items()}
        for future in concurrent.futures.as_completed(player_futures):
            uname, weight = future.result()
            players[uname] = weight
    return players

def main():
    choose = input("Do you want to get player weights from tracker.gg, or input them manually? (T for tracker.gg, M for manually): ").lower()

    if choose == "t":
        player_n = 0
        usernames = {}
        while len(usernames) < 10:
            player_n += 1
            position = num2words(player_n, ordinal=True)
            userin = input(f"{position} player's username (no spaces between username and tag): ")
            splitted = re.split(r'#', userin)
            riottag = splitted[-1]
            splitted.remove(riottag)
            riotname = str(*splitted)
            usernames[riotname] = riottag

        players = get_player_weights(usernames)
        print(players)

    elif choose == "m":
        player_n = 0
        players = {}
        while len(players) < 10:
            player_n += 1
            position = num2words(player_n, ordinal=True)
            userin = input(f"{position} player's name & score. Separate with comma (ex: 'SEN curry, 0.743): ")
            splitted = re.split(r', ', userin)

            scorestr = splitted[-1]
            score = float(splitted[-1])
            splitted.remove(scorestr)

            name = str(*splitted)
            players[name] = score

        print(players)

    while True:
        try:
            debuff = input("Do you want to change any weights? (yes/no): ").lower()

            if debuff == "yes":
                debuff = input("example: 'nerf ranchbleam: 0.2'. this will subtract 0.2 from ranchbleam. saying 'buff' will add instead.): ")
                if "nerf" in debuff:
                    splitted = re.split(r'nerf ', debuff)
                    playername, debuffvalue = re.split(r': ', splitted[1])
                    debuffvalue = float(debuffvalue)
                    players[playername] = max(0, players[playername] - debuffvalue)
                    print(players)
                elif "buff" in debuff:
                    splitted = re.split(r'buff ', debuff)
                    playername, debuffvalue = re.split(r': ', splitted[1])
                    debuffvalue = float(debuffvalue)
                    players[playername] = min(1, players[playername] + debuffvalue)
                    print(players)
            else:
                break
        except Exception as e:
            print(f"Invalid input, {e}")

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

if __name__ == "__main__":
    main()
