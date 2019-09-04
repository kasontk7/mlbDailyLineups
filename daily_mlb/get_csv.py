import webbrowser
import datetime
import sys

now = datetime.datetime.now()
today_date = now.strftime("%Y-%m-%d")
#today_date = "2019-06-16"

todays_pitchers_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
todays_pitchers_last30_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season=2019&month=3&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
todays_pitchers_home_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=15&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
todays_pitchers_away_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=16&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
todays_pitchers_vsleft_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=13&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
todays_pitchers_vsright_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2019&month=14&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=p"
relief_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=8&season=2019&month=0&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=15,d"
relief_last30_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=8&season=2019&month=3&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0"
wrc_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=0&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=19,d"
ops_last7_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=1&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"
ops_last30_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=3&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"
left_ops_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=13&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"
right_ops_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=14&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"
home_ops_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=15&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"
away_ops_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2019&month=16&season1=2019&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&sort=9,d"

webbrowser.open(todays_pitchers_url + today_date)
webbrowser.open(todays_pitchers_last30_url + today_date)
webbrowser.open(todays_pitchers_home_url + today_date)
webbrowser.open(todays_pitchers_away_url + today_date)
webbrowser.open(todays_pitchers_vsleft_url + today_date)
webbrowser.open(todays_pitchers_vsright_url + today_date)
webbrowser.open(ops_last7_url)

if len(sys.argv) > 1:
	webbrowser.open(ops_last30_url)
	webbrowser.open(relief_last30_url)
	webbrowser.open(relief_url)
	webbrowser.open(wrc_url)
	webbrowser.open(left_ops_url)
	webbrowser.open(right_ops_url)
	webbrowser.open(home_ops_url)
	webbrowser.open(away_ops_url)

