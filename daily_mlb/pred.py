import requests
from bs4 import BeautifulSoup
import csv
from tabulate import tabulate
import operator

def print_error_msg():
    error_str = "ERROR "
    for i in range(3):
        error_str = error_str + error_str
    for i in range(3):
        print(error_str)

def print_underline(text):
    end = "\033[0m"
    underline = "\033[4m"
    return(underline + text + end)

def print_avg_bold(text):
    end = "\033[0m"
    bold = "\033[4m"
    if float(text) > 0.049:
        return(bold + text + end)
    return(text)

def print_era_bold(text):
    end = "\033[0m"
    bold = "\033[4m"
    if float(text) > 1 or float(text) < -1:
        return(bold + text + end)
    return(text)

def print_rank_color(text):
    end = "\033[0m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    red = "\033[0;31m"
    if int(text) < 10:
        return(green + text + end)
    elif int(text) < 20:
        return(yellow + text + end)
    else:
        return(red + text + end)

def convert_EST_to_PST(time):
    seperate = time.split(':')
    new_hour = int(seperate[0])
    if (new_hour < 12):
        new_hour += 12
    new_hour -= 3
    return (str(new_hour) + ":" + seperate[1])

def get_gamelog_and_summary(stats_table):
    # check if pitcher has 2019 starts
    gamelog = [] # date, location, pitches, IP, ER, Hits, BB, SO, OPP, Opp WrC, BallPark Fctr
    gamelog_summary = [0, 0, 0, 0] # init ip, ipremainder, total er, total bb+hits
    if stats_table is None:
            return (gamelog, gamelog_summary)
    all_rows = stats_table.find_all('tr')
    for row in reversed(all_rows):
        datums = row.find_all('td')
        if (row['class'][0] == 'row1' or row['class'][0] == 'row2') and len(datums) > 12:
            date = datums[0].get_text()[:-1]
            location = "Away"
            if datums[1].get_text().split(' ')[0] == "vs":
                location = "Home"
            pitchers_thrown = int(datums[10].get_text())
            ip = datums[3].get_text()
            ip_list = ip.split('.')
            if len(ip_list) < 2:
                continue
            ip_first = int(ip_list[0])
            ip_remainder = int(ip_list[1])
            er = int(datums[6].get_text())
            hits = int(datums[4].get_text())
            bb = int(datums[8].get_text())
            so = int(datums[9].get_text())
            opp = datums[1].find('a').get_text()
            opp_wrc = wrc_dict[abbrev_dict[opp]][0]
            #ballpark_fctr = TODO
            gamelog_summary[0] += ip_first
            gamelog_summary[1] += ip_remainder
            gamelog_summary[2] += er
            gamelog_summary[3] += hits + bb
            game_data = [date, location, pitchers_thrown, ip, er, hits, bb, so, opp, opp_wrc]
            gamelog.append(game_data)
            if len(gamelog) == 7:
                break
    if len(gamelog) > 0:
        total_ip = gamelog_summary[0] + gamelog_summary[1]//3
        total_ip = float(str(total_ip) + '.' + str(gamelog_summary[1]%3))
        era = gamelog_summary[2]/total_ip*9
        whip = gamelog_summary[3]/total_ip
        gamelog_summary = [total_ip/len(gamelog), whip, era]
    return (gamelog, gamelog_summary)

def get_dict_from_csv(csv_name, key_row, sorted_row, other_rows, max_first, header_exists):
    return_dict = {}
    rank = 1
    with open('csv/' + csv_name,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        if header_exists:
            header = next(csvreader)
        sortedlist = sorted(csvreader, key=lambda row: float(row[sorted_row]), reverse=max_first)
        for line in sortedlist:
            name = line[key_row]
            return_dict[name] = [rank, float(line[sorted_row])]
            for index in other_rows:
                return_dict[name].append(line[index])
            rank += 1
    return return_dict

team_colors = ["Red", "White", "Blue"]
starter_ovr_dict = get_dict_from_csv('todays_pitchers.csv',0,18,[6,2,3,15,17],True,True) # GS,W,L,ERA,xFIP
starter_last30_dict = get_dict_from_csv('todays_pitchers_last30.csv',0,18,[6,2,3,15,17],True,True)
starter_vsleft_dict = get_dict_from_csv('todays_pitchers_vsleft.csv',0,9,[10,13,16],False,True) # WHIP, ERA, xFIP
starter_vsright_dict = get_dict_from_csv('todays_pitchers_vsright.csv',0,9,[10,13,16],False,True)
starter_home_dict = get_dict_from_csv('todays_pitchers_home.csv',0,13,[9,10,16],False,True) #Avg, WHIP, xFIP
starter_away_dict = get_dict_from_csv('todays_pitchers_away.csv',0,13,[9,10,16],False,True)
relief_dict = get_dict_from_csv('relief.csv',0,14,[],False,True)
relief_last30_dict = get_dict_from_csv('relief_last30.csv',0,14,[],False,True)
wrc_dict = get_dict_from_csv('wrc.csv',0,18,[],True,True)
leftops_dict = get_dict_from_csv('leftops.csv',0,8,[],True,True)
rightops_dict = get_dict_from_csv('rightops.csv',0,8,[],True,True)
homeops_dict = get_dict_from_csv('homeops.csv',0,8,[],True,True)
awayops_dict = get_dict_from_csv('awayops.csv',0,8,[],True,True)
last7ops_dict = get_dict_from_csv('last7ops.csv',0,8,[],True,True)
last30ops_dict = get_dict_from_csv('last30ops.csv',0,8,[],True,True)

abbrev_dict = {}
with open('csv/abbrevs.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for line in csvreader:
        brevteam = line[0].split("|")
        abbrev_dict[brevteam[0]] = brevteam[1]

name_dict = {}
with open('csv/name_change.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for line in csvreader:
        name = line[0]
        name_dict[name] = line[1]

url = "https://www.cbssports.com"
extension = "/mlb/probable-pitchers/"
# extension += "20190615"
doc = requests.get(url + extension)
soup = BeautifulSoup(doc.text, 'html.parser')

game_boxes = soup.find_all('div', class_='gameContainer')
for game in game_boxes:
    matchup_teams = game.find('span', class_='titleGame').get_text().split(' vs. ')
    time = game.find('span', class_='subtitleGame').get_text().split(' ')[0]
    time = convert_EST_to_PST(time)

    away_team_full_name = matchup_teams[0]
    away_team_short_name = away_team_full_name.split(' ')[-1]
    if away_team_full_name.split(' ')[-2] in team_colors:
        away_team_short_name = away_team_full_name.split(' ')[-2] + " " + away_team_short_name
    away_pitcher_html = game.find('div', class_='pitcher left')
    away_pitcher_html_info = away_pitcher_html.find_all('ul')

    away_pitcher_name = away_pitcher_html_info[0].find_all('li')
    away_pitcher_firstname = away_pitcher_name[0].get_text()
    away_pitcher_lastname = away_pitcher_name[1].get_text()
    away_pitcher_full_name = away_pitcher_firstname + " " + away_pitcher_lastname
    if away_pitcher_full_name in name_dict.keys():
        away_pitcher_full_name = name_dict[away_pitcher_full_name]
    away_pitcher_hand = away_pitcher_name[2].get_text().split(' ')[0]

    away_pitcher_links = away_pitcher_html_info[1].find_all('li')
    away_pitcher_gamelog_link = away_pitcher_links[1].find('a')['href']
    away_pitcher_splits = away_pitcher_links[2].find('a')['href']

    away_pitcher_gamelog_doc = requests.get(url + away_pitcher_gamelog_link)
    soup = BeautifulSoup(away_pitcher_gamelog_doc.text, 'html.parser')
    stats_table = soup.find('table', class_='data borderTop title')
    away_pitcher_gamelog, away_pitcher_gamelog_summary = get_gamelog_and_summary(stats_table)
    # -------------------------------------------------------------------------------
    home_team_full_name = matchup_teams[1]
    home_team_short_name = home_team_full_name.split(' ')[-1]
    if home_team_full_name.split(' ')[-2] in team_colors:
        home_team_short_name = home_team_full_name.split(' ')[-2] + " " + home_team_short_name
    home_pitcher_html = game.find('div', class_='pitcher right')
    home_pitcher_html_info = home_pitcher_html.find_all('ul')

    home_pitcher_name = home_pitcher_html_info[0].find_all('li')
    home_pitcher_firstname = home_pitcher_name[0].get_text()
    home_pitcher_lastname = home_pitcher_name[1].get_text()
    home_pitcher_full_name = home_pitcher_firstname + " " + home_pitcher_lastname
    if home_pitcher_full_name in name_dict.keys():
        home_pitcher_full_name = name_dict[home_pitcher_full_name]
    home_pitcher_hand = home_pitcher_name[2].get_text().split(' ')[0]

    home_pitcher_links = home_pitcher_html_info[1].find_all('li')
    home_pitcher_gamelog_link = home_pitcher_links[1].find('a')['href']
    home_pitcher_splits = home_pitcher_links[2].find('a')['href']

    home_pitcher_gamelog_doc = requests.get(url + home_pitcher_gamelog_link)
    soup = BeautifulSoup(home_pitcher_gamelog_doc.text, 'html.parser')
    stats_table = soup.find('table', class_='data borderTop title')
    home_pitcher_gamelog, home_pitcher_gamelog_summary = get_gamelog_and_summary(stats_table)


    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print(time + " " + away_team_full_name + " @ " + home_team_full_name)
    print()
    print(print_underline(home_team_short_name + " Pitcher: " + home_pitcher_full_name + " " + home_pitcher_hand))
    if (home_pitcher_full_name) not in starter_ovr_dict.keys():
        print("No Pitcher Data")
    else:
        print("2019 Season: " + starter_ovr_dict[home_pitcher_full_name][2] + "GS " + starter_ovr_dict[home_pitcher_full_name][3] + "-" + starter_ovr_dict[home_pitcher_full_name][4] + " | " + starter_ovr_dict[home_pitcher_full_name][5] + " ERA | " + str(starter_ovr_dict[home_pitcher_full_name][1]) + "WAR | Rank: " + str(starter_ovr_dict[home_pitcher_full_name][0]))
        if (home_pitcher_full_name) in starter_last30_dict.keys():
            print("   Last  30: " + starter_last30_dict[home_pitcher_full_name][2] + "GS " + starter_last30_dict[home_pitcher_full_name][3] + "-" + starter_last30_dict[home_pitcher_full_name][4] + " | " + starter_last30_dict[home_pitcher_full_name][5] + " ERA | " + str(starter_last30_dict[home_pitcher_full_name][1]) + "WAR | Rank: " + str(starter_last30_dict[home_pitcher_full_name][0]))
        lefty_avg = float(starter_vsleft_dict[home_pitcher_full_name][1])
        righty_avg = float(starter_vsright_dict[home_pitcher_full_name][1])
        if home_pitcher_hand == "RHP":
            avg_diff = lefty_avg - righty_avg
            print("Diff in Avg. " + print_avg_bold("{:.3f}".format(avg_diff)) + " Lefty: " + "{:.3f}".format(lefty_avg) + " (Righty: " + "{:.3f}".format(righty_avg) + ")")    
        else:
            avg_diff = righty_avg - lefty_avg
            print("Diff in Avg. " + print_avg_bold("{:.3f}".format(avg_diff)) + " Righty: " + "{:.3f}".format(righty_avg) + " (Lefty: " + "{:.3f}".format(lefty_avg) + ")")
        if home_pitcher_full_name in starter_home_dict.keys() and home_pitcher_full_name in starter_away_dict.keys():
            home_era = float(starter_home_dict[home_pitcher_full_name][1])
            away_era = float(starter_away_dict[home_pitcher_full_name][1])
            era_diff = home_era - away_era
            print("Diff in ERA: " + print_era_bold("{:.2f}".format(era_diff)) + " Home: " + "{:.2f}".format(home_era) + " (Away: " + "{:.2f}".format(away_era) + ")")    
        print(home_pitcher_full_name + " Last " + str(len(home_pitcher_gamelog)) + " Games:")
        game_log_header = ['Date', '@', 'Pitches', 'IP', 'ER','Hits','BB','SO','OPP','wRC+']
        print(tabulate(home_pitcher_gamelog, headers=game_log_header, tablefmt='orgtbl'))
        print("{:.2f}".format(home_pitcher_gamelog_summary[0]) + "IP | " + "{:.2f}".format(home_pitcher_gamelog_summary[1]) + "WHIP | " + "{:.2f}".format(home_pitcher_gamelog_summary[2]) + "ERA")
    print(home_team_short_name + " Relief ERA: " + "{:.2f}".format(relief_dict[home_team_short_name][1]) + " Rank: " + str(relief_dict[home_team_short_name][0]) + " | Last30 ERA: " + "{:.2f}".format(relief_last30_dict[home_team_short_name][1]) + " Rank: " + str(relief_last30_dict[home_team_short_name][0]))
    print(print_underline(away_team_short_name + " Batting:"))       
    awayops = awayops_dict[away_team_short_name][1]
    homeops = homeops_dict[away_team_short_name][1]
    ops_diff = awayops - homeops
    print("Away OPS: " + "{:.3f}".format(awayops) + " Rank: " + print_rank_color(str(awayops_dict[away_team_short_name][0])) + " | Diff: " + "{:.3f}".format(awayops - homeops) + " (Home Rank: " + str(homeops_dict[away_team_short_name][0]) + ")")
    rightops = rightops_dict[away_team_short_name][1]
    leftops = leftops_dict[away_team_short_name][1]
    if home_pitcher_hand == "RHP":
        print("OPS against Righties: " + "{:.3f}".format(rightops) + " Rank: " + print_rank_color(str(rightops_dict[away_team_short_name][0])) + " | Diff: " + "{:.3f}".format(rightops - leftops) + " (Vs. Left Rank: " + str(leftops_dict[away_team_short_name][0]) + ")")
    else:
        print("OPS against Lefties: " + "{:.3f}".format(leftops) + " Rank: " + print_rank_color(str(leftops_dict[away_team_short_name][0])) + " | Diff: " + "{:.3f}".format(leftops - rightops) + " (Vs. Right Rank: " + str(rightops_dict[away_team_short_name][0]) + ")")
    print("wRC+ Rank: " + print_rank_color(str(wrc_dict[away_team_short_name][0])) + " | Last7OPS: " + "{:.3f}".format(last7ops_dict[away_team_short_name][1]) + " Rank: " + print_rank_color(str(last7ops_dict[away_team_short_name][0])) + " | Last30OPS: " + "{:.3f}".format(last30ops_dict[away_team_short_name][1]) + " Rank: " + print_rank_color(str(last30ops_dict[away_team_short_name][0])))
    print()
    print(print_underline(away_team_short_name + " Pitcher: " + away_pitcher_full_name + " " + away_pitcher_hand))
    if (away_pitcher_full_name) not in starter_ovr_dict.keys():
        print("No Pitcher Data")
    else:
        print("2019 Season: " + starter_ovr_dict[away_pitcher_full_name][2] + "GS " + starter_ovr_dict[away_pitcher_full_name][3] + "-" + starter_ovr_dict[away_pitcher_full_name][4] + " | " + starter_ovr_dict[away_pitcher_full_name][5] + " ERA | " + str(starter_ovr_dict[away_pitcher_full_name][1]) + "WAR | Rank: " + str(starter_ovr_dict[away_pitcher_full_name][0]))
        if (away_pitcher_full_name) in starter_last30_dict.keys():
            print("   Last  30: " + starter_last30_dict[away_pitcher_full_name][2] + "GS " + starter_last30_dict[away_pitcher_full_name][3] + "-" + starter_last30_dict[away_pitcher_full_name][4] + " | " + starter_last30_dict[away_pitcher_full_name][5] + " ERA | " + str(starter_last30_dict[away_pitcher_full_name][1]) + "WAR | Rank: " + str(starter_last30_dict[away_pitcher_full_name][0]))
        lefty_avg = float(starter_vsleft_dict[away_pitcher_full_name][1])
        righty_avg = float(starter_vsright_dict[away_pitcher_full_name][1])
        if away_pitcher_hand == "RHP":
            avg_diff = lefty_avg - righty_avg
            print("Diff in Avg. " + print_avg_bold("{:.3f}".format(avg_diff)) + " Lefty: " + "{:.3f}".format(lefty_avg) + " (Righty: " + "{:.3f}".format(righty_avg) + ")")    
        else:
            avg_diff = righty_avg - lefty_avg
            print("Diff in Avg. " + print_avg_bold("{:.3f}".format(avg_diff)) + " Righty: " + "{:.3f}".format(righty_avg) + " (Lefty: " + "{:.3f}".format(lefty_avg) + ")")
        if away_pitcher_full_name in starter_home_dict.keys() and away_pitcher_full_name in starter_away_dict.keys():
            away_era = float(starter_away_dict[away_pitcher_full_name][1])
            home_era = float(starter_home_dict[away_pitcher_full_name][1])
            era_diff = away_era - home_era
            print("Diff in ERA: " + print_era_bold("{:.2f}".format(era_diff)) + " Away: " + "{:.2f}".format(away_era) + " (Home: " + "{:.2f}".format(home_era) + ")")    
        print(away_pitcher_full_name + " Last " + str(len(away_pitcher_gamelog)) + " Games:")
        game_log_header = ['Date', '@', 'Pitches', 'IP', 'ER','Hits','BB','SO','OPP','wRC+']
        print(tabulate(away_pitcher_gamelog, headers=game_log_header, tablefmt='orgtbl'))
        print("{:.2f}".format(away_pitcher_gamelog_summary[0]) + "IP | " + "{:.2f}".format(away_pitcher_gamelog_summary[1]) + "WHIP | " + "{:.2f}".format(away_pitcher_gamelog_summary[2]) + "ERA")
    print(away_team_short_name + " Relief ERA: " + "{:.2f}".format(relief_dict[away_team_short_name][1]) + " Rank: " + str(relief_dict[away_team_short_name][0]) + " | Last30 ERA: " + "{:.2f}".format(relief_last30_dict[away_team_short_name][1]) + " Rank: " + str(relief_last30_dict[away_team_short_name][0]))
    print(print_underline(home_team_short_name + " Batting:"))   
    homeops = homeops_dict[home_team_short_name][1]
    awayops = awayops_dict[home_team_short_name][1]
    ops_diff = homeops - awayops
    print("Home OPS: " + "{:.3f}".format(homeops) + " Rank: " + print_rank_color(str(homeops_dict[home_team_short_name][0])) + " | Diff: " + "{:.3f}".format(homeops - awayops) + " (Away Rank: " + str(awayops_dict[home_team_short_name][0]) + ")")
    rightops = rightops_dict[home_team_short_name][1]
    leftops = leftops_dict[home_team_short_name][1]
    if away_pitcher_hand == "RHP":
        print("OPS against Righties: " + "{:.3f}".format(rightops) + " Rank: " + print_rank_color(str(rightops_dict[home_team_short_name][0])) + " | Diff: " + "{:.3f}".format(rightops - leftops) + " (Vs. Left Rank: " + str(leftops_dict[home_team_short_name][0]) + ")")
    else:
        print("OPS against Lefties: " + "{:.3f}".format(leftops) + " Rank: " + print_rank_color(str(leftops_dict[home_team_short_name][0])) + " | Diff: " + "{:.3f}".format(leftops - rightops) + " (Vs. Right Rank: " + str(rightops_dict[home_team_short_name][0]) + ")")
    print("wRC+ Rank: " + print_rank_color(str(wrc_dict[home_team_short_name][0])) + " | Last7OPS: " + "{:.3f}".format(last7ops_dict[home_team_short_name][1]) + " Rank: " + print_rank_color(str(last7ops_dict[home_team_short_name][0])) + " | Last30OPS: " + "{:.3f}".format(last30ops_dict[home_team_short_name][1]) + " Rank: " + print_rank_color(str(last30ops_dict[home_team_short_name][0])))



















