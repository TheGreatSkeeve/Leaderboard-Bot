from logger import *
from time import sleep
import praw
from pathlib import Path

# Set the name and location of the database
dbname = "info.db"
dbfolder = "db/"

# Initialize a variable to store leaderboard stats in
leaderboard_dict = {}

# This makes the database folder if it doesn't exist
Path(dbfolder).mkdir(parents=True, exist_ok=True)


# Bot's username
bot_username = "SimonSkinnerBot"

# Admin
consoleoutput = ["\nLeaderboard bot is running\n"] # Strings to print to the console to help with general awareness

# Sign into Reddit
# Using another bot of mine to test, too lazy to make a new one
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="TheGreatSkeeve_",
    username=bot_username
)

# Set the subreddit to read comments / posts from
target_sub = "the_greater_good"
subreddit = reddit.subreddit(target_sub)



# Function to send a message to Telegram group configured in the SECRETS.py file
def sendMessage(message):
    import requests
    msg1 = "https://api.telegram.org/bot"
    msg2 = "/sendMessage?chat_id="
    msg3 = "&text="
    URL = msg1+token+msg2+chatid+msg3+message
    r = requests.get(url=URL)


# Function to respond if we're rate-limited
# This doesn't happen much unless it's a new account, or you're spamming
def rateLimit(error,comment):
    timeleft = ((error.split("try again in "))[1].split(" minute"))[0]
    part_1 = "We're being rate-limited...stupid Reddit."
    part_2 = error
    part_3 = "Sleeping for " + timeleft + " minutes until I can comment again..."
    link = "(" + str(comment.permalink) + ")"
    outOfJail = "Okay, ratelimit should be over"
    message = part_1 + "\n" + link + "\n" + part_2 + "\n" + part_3
    sendMessage(message)
    sendMessage(link)
    sleep((int(timeleft) * 60) + 1)
    sendMessage(outOfJail)


# Let Telegram know we're running
sendMessage("Simon Skinner is powering up")

# Let the console know we're running
print(consoleoutput[0])

'''
Counting Upvotes

The actual counting will take shape like this, the bot can stream
comments / posts and record the upvote count for each.  Need to
look up the code, though.

One processed, this will spit out an array of the top 100 comments and top 100 posts
from a varying length of time, along with the user and the upvote count

Another function will take this data and organize it into a table, then 
post it as a comment on the sub.

'''
for comment in subreddit.stream.comments():
    print("In progress")

for submission in subreddit.stream:
    print("In progress")


'''
Updating the Sidebar

Seems like this is possible, but the bot must be a mod for the sub.

'''

subreddit.mod.update(description="new sidebar goes here")

old_sidebar = subreddit.mod.settings()['description']
