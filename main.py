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
testsubreddit = reddit.subreddit(testsub)


def wiki_create(pageName,content,reason):
    subreddit.wiki.create(pageName,content=content, reason=reason)


def wiki_setup(subreddit):
    pagename=["2020-Leaderboard","2021-Leaderboard"]
    content=["2020 Leaderboard","2021 Leaderboard"]
    reason="Initial Wiki Leaderboard Setup"
    for i in range(0,len(pagename)):
        subreddit.wiki.create(pagename[i],content[i],reason)


def newTextWidget(subreddit,title,content):
    widgets = subreddit.widgets
    styles = {"backgroundColor": "#FFFF66", "headerColor": "#3333EE"}
    text_area = widgets.mod.add_text_area(title,content, styles)

# newTextWidget(subreddit, "Monthly Leaderboard","Pending")

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

# There is wholeheartedly a better way to do this.
def getPosts(subreddit,timerange):

    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = '|User|Score|\n|:-:|:-:|\n'
    info = []
    timerange = "month"
    submissions = testsubreddit.top(timerange,limit=250)
    done=False
    for submission in submissions:
        if len(info)>0:
            print(len(info))
            for i in range(0,len(info)):
                try:
                    val = info[i].index(str(submission.author))
                    info[val][1] = info[val][1] + submission.score
                    done=True
                except:
                    pass
        else:
            info.append([str(submission.author), submission.score])
        if done==False:
            info.append([str(submission.author), submission.score])

    total = 0
    for i in range(0,len(info)):
        try:
            loc = info[i].index("GaramaMasala2020")
            total = total + info[loc][1]
        except:
            pass



    submissions_Top = sorted(info, key=itemgetter(1),reverse=True)
    info = []
    for submission in submissions_Top:
        user="u/"+submission[0]
        score=str(submission[1])
        row=user+"|"+score+"\n"
        info.append(row)
    for i in range(0,len(info)):
        Header = Header + info[i]
    Header = Header+status
    return Header

def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)



def main():
    while True:
        widget = getWidget(subreddit)
        widget.mod.update(text=getPosts(testsubreddit,"month"))
        healthCheckerPing()
        sleep(15)

main()