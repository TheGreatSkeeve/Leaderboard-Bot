from time import sleep
from operator import itemgetter
from datetime import datetime

from secret import *

target_sub = "the_greater_good"
subreddit = reddit.subreddit(target_sub)




def getWidget():
    widgets = reddit.subreddit("the_greater_good").widgets
    text_area = [None,None,None]
    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.TextArea):
            if widget.shortName == "Post Leaderboard (Weekly)":
                text_area[0] = widget
            if widget.shortName == "Comment Leaderboard (Weekly)":
                text_area[1] = widget
            if widget.shortName == "Post Leaderboard (Daily)":
                text_area[2] = widget
    return text_area


def getPosts(timerange):
    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = '|User|Score|\n|:-:|:-:|\n'
    info = []
    for submission in reddit.subreddit("pantypeel").top(timerange,limit=250):
        if submission.score > 100:
            info.append([str(submission.author),submission.score,str(submission.url)])
    submissions_Top = sorted(info, key=itemgetter(1),reverse=True)
    info = []
    for submission in submissions_Top:
        user="u/"+submission[0]
        score=str(submission[1])
        url=submission[2]
        row=user+"|["+score+"]("+url+")\n"
        info.append(row)
    for i in range(0,len(info)):
        Header = Header + info[i]
    Header = Header+status
    return Header

def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)

def getComments(posts,timescale,subreddit,scorelimit):
    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = '|User|Score|\n|:-:|:-:|\n'
    commentlist = []
    for submission in reddit.subreddit(subreddit).top(timescale, limit=posts):
        if submission.score > 20:
            for comment in submission.comments.list():
                if comment.score>scorelimit:
                        commentlist.append([str(comment.author),comment.score,str(comment.permalink)])
            comments_Top = sorted(commentlist, key=itemgetter(1), reverse=True)
            info = []
    for comment in comments_Top:
        user = "u/" + comment[0]
        score = str(comment[1])
        url = "https://reddit.com/"+comment[2]
        row = user + "|[" + score + "](" + url + ")\n"
        info.append(row)
    for i in range(0, len(info)):
        Header = Header + info[i]
    Header = Header + status
    return Header


def main():
    while True:
        widgets = getWidget()
        postUpdateWeek = widgets[0].mod.update(text=getPosts("week"))
        postUpdateDay = widgets[2].mod.update(text=getPosts("day"))
        commentUpdate = widgets[1].mod.update(text=getComments(50,"week","pantypeel",5))
        healthCheckerPing()
        sleep(60)

main()