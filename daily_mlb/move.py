import os
from pathlib import Path

fangraph_path = Path("/Users/kasonkang/Downloads/FanGraphs Leaderboard.csv")
fangraph_path2 = Path("/Users/kasonkang/Downloads/FanGraphs Leaderboard (7).csv")

if fangraph_path.exists():
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard.csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (1).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers_last30.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (2).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers_home.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (3).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers_away.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (4).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers_vsleft.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (5).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/todays_pitchers_vsright.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (6).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/last7ops.csv")

if fangraph_path2.exists():
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (7).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/last30ops.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (8).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/relief_last30.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (9).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/relief.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (10).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/wrc.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (11).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/leftops.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (12).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/rightops.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (13).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/homeops.csv")
	os.rename("/Users/kasonkang/Downloads/FanGraphs Leaderboard (14).csv", "/Users/kasonkang/Documents/Projects/daily_mlb/csv/awayops.csv")