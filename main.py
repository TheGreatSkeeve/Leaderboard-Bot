from time import sleep
from operator import itemgetter
from datetime import datetime
import praw

from secret import *

data = redditsignin()

reddit = praw.Reddit(
    client_id=data[0],
    client_secret=data[1],
    password=data[2],
    user_agent=data[3],
    username=data[3],
)

subreddit = reddit.subreddit(target_sub)
subreddit_test = reddit.subreddit(target_sub_test)


def wiki_create(pageName,content,reason):
    subreddit.wiki.create(pageName,content=content, reason=reason)


def wiki_setup(subreddit):
    pagename=["2020-Leaderboard","2021-Leaderboard"]
    content=["2020 Leaderboard","2021 Leaderboard"]
    reason="Initial Wiki Leaderboard Setup"
    for i in range(0,len(pagename)):
        subreddit_test.wiki.create(pagename[i],content[i],reason)


def newTextWidget(subreddit,title,content):
    widgets = subreddit.widgets
    styles = {"backgroundColor": "#FFFF66", "headerColor": "#3333EE"}
    text_area = widgets.mod.add_text_area(title,content, styles)

# newTextWidget(subreddit, "Monthly Leaderboard","Pending")

def editWiki(subreddit,content,page="2021-Leaderboard"):
    page = subreddit.wiki[page]
    page.edit(content)


page = subreddit.wiki['index']

def getWidget(subreddit):
    widgets = subreddit.widgets
    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.TextArea):
            if widget.shortName == "Monthly Leaderboard":
                text_area = widget
    return text_area

# Run this, assign to a variable to get the raw markup to update the widget with
# This is super specialized, need to break it up
# Need to set some kind of config file, too..


def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)

def getScores(subreddit,timerange,limit):
    # Gets the top 250 posts
    submissions = subreddit.top(timerange,limit=limit)
    info = []

    # Big loop to find users and posts and scores
    for submission in submissions:
        user=submission.author
        if str(user)=="None":
            pass
        else:
            score=submission.score
            now = datetime.now().strftime('%m')
            month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
            if timerange=="all":
                now=month
            if now==month:
                # If no posts have been added yet, append the first user
                if info == []:
                    info.append([user,score])
                else:
                    found=False
                    # Search through the info array to see if the username exists.  Add the score to that user's score, or
                    # add that user and their base score to the info array
                    for i in range(0,len(info)):
                        if user==info[i][0]:
                            found=True
                            info[i][1] = info[i][1] + score
                    if found==False:
                        info.append([user,score])
    info = sorted(info, key=itemgetter(1),reverse=True)
    return info

def makeTable(info):
    table = []
    for i in range(0,len(info)):
        user="u/"+str(info[i][0])
        score=str(info[i][1])
        number="#"+str(i+1)
        row=number+"|"+user+"|"+score+"\n"
        table.append(row)
    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = '|Place|User|Score|\n|:-:|:-:|:-:|\n'
    if len(table)>24:
        x=25
    else:
        x=len(table)
    for i in range(0,x):
        Header = Header + table[i]
    table = Header+status
    return table

def main():
    while True:
        # Update Sidebar
        monthly = makeTable(getScores(subreddit,"month", 250))
        widget = getWidget(subreddit_test)
        widget.mod.update(text=monthly)
        print("Sidebar updated")

        # Update Wiki
        alltime=makeTable(getScores(subreddit,"all",10000))
        editWiki(subreddit_test, alltime)
        sleep(60)

main()