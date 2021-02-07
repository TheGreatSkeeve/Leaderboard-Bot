def findSubString(comment,text):
    numstart = comment.index(text)
    numend = numstart + 16
    replytext = comment[numstart:numend]
    return replytext

def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)


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


for submission in submissions:
    x = submission.created
    ts = int(x)
    print(ts)
    month = datetime.utcfromtimestamp(ts).strftime('%m')
    print(month)
    if month == "02":
        print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
