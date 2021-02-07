
# There is wholeheartedly a better way to do this.
def getPosts(subreddit,timerange):

    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = '|User|Score|\n|:-:|:-:|\n'
    info = []
    timerange = "month"
    submissions = subreddit.top(timerange,limit=250)
    info = [[],[]]
    for submission in submissions:
        user=submission.author
        score=submission.score
        now = datetime.now().strftime('%m')
        month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
        if now==month:
            if info == [[], []]:
                info.append([user,score])
            else:
                found=False
                for i in range(0,len(info)):
                    if user==info[i][0]:
                        found=True
                        info[i][1] = info[i][1] + score
                if found==False:
                    info.append([user,score])





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