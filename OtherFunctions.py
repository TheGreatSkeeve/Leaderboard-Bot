def findSubString(comment,text):
    numstart = comment.index(text)
    numend = numstart + 16
    replytext = comment[numstart:numend]
    return replytext

def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)
