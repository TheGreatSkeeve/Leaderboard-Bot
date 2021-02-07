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


# Get the users and scores
# posts = getScores(subreddit, "month")
def getScores(subreddit,timerange):
    # Gets the top 250 posts
    submissions = subreddit.top(timerange,limit=250)
    info = []

    # Big loop to find users and posts and scores
    for submission in submissions:
        user=submission.author
        score=submission.score
        now = datetime.now().strftime('%m')
        month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
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
    return info


def main():
        widget = getWidget(subreddit)
        posts = getScores(subreddit,"month")
        print(posts)
        # widget.mod.update(text=getPosts(testsubreddit,"month"))
        # healthCheckerPing()
        # sleep(15)

main()