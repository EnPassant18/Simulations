import random
import numpy
from os import system
from tabulate import tabulate
from statistics import mode
Points=False

# PROGRAM SETTINGS:
roundsList=[3,4,5,6,8,10,12,16,20,24]
rtgStdList=[.1,.2,.3,.4,.5,.75,1,1.5]
tournaments=2000
players=50 # Must be even
testing=1

# Ranking Algorithms
def sk(): #Solkoff
    global Points
    Points=True
    global db
    for plr in range(players):
        db[plr][7]=sum([db[db[plr][3][opp]][4] for opp in range(rd+1)])
    for plr in range(players):
        db[plr][8]=sum([db[db[plr][3][opp]][7] for opp in range(rd+1)])
    for plr in range(players):
        db[plr][9]=sum([db[db[plr][3][opp]][8] for opp in range(rd+1)])

def BT(Reset=True):
    global Points
    Points=False
    global db
    if Reset:
        for plr in range(players):
           db[plr][7]=1
    its=iters[roundsList.index(rounds)][rtgStdList.index(rtgStd)]
    for it in range(its):
        ratings=[]
        for plr in range(players):
            if db[plr][4]==0:
                ratings.append(0)
            elif db[plr][7]==0:
                db[plr][7]=1/(rd+1)
                ratings.append(db[plr][4]/sum([1/(db[db[plr][3][opp]][7]+db[plr][7]) for opp in range(rd+1)]))
            else:
                ratings.append(db[plr][4]/sum([1/(db[db[plr][3][opp]][7]+db[plr][7]) for opp in range(rd+1)]))
        for plr in range(players):
            db[plr][7]=ratings[plr]

def kw(): #Kendall-Wei
    global Points
    Points=False
    global db
    for plr in range(players):
        db[plr][7]=sum([db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==1])
    for it in range(25):
        scores=[sum([db[db[plr][3][i]][7] for i in range(rd+1) if db[plr][2][i]==1]) for plr in range(players)]
        for plr in range(players):
            db[plr][7]=scores[plr]
        print(Eval())

def gd(): #Goddard
    global Points
    Points=False
    global db
    for plr in range(players):
            db[plr][7]=db[plr][4]
    for it in range(25):
        scores=[sum([db[db[plr][3][i]][7]+db[plr][7] for i in range(rd+1) if db[plr][2][i]==1]) for plr in range(players)]
        for plr in range(players):
            db[plr][7]=scores[plr]
        print(Eval())
        
iters=[[2,2,2,2,2,2,2,2],
       [2,2,2,2,2,2,2,2],
       [2,2,2,2,2,2,2,2],
       [2,2,2,2,2,2,2,2],
       [2,2,2,2,2,2,2,3],
       [2,2,2,2,2,2,2,3],
       [2,2,2,2,2,2,3,3],
       [2,2,2,2,2,2,3,3],
       [2,2,2,2,2,3,3,3],
       [2,2,2,2,2,3,3,3]]
def kwr(): #Kendall-Wei revised
    global Points
    Points=False
    global db
    its=iters[roundsList.index(rounds)][rtgStdList.index(rtgStd)]
    for plr in range(players):
        db[plr][7]=sum([db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==0])
        db[plr][8]=sum([rounds-db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==0])
    for it in range(its):
        scores=[sum([db[db[plr][3][i]][7] for i in range(rd+1) if db[plr][2][i]==1]) for plr in range(players)]
        for plr in range(players):
            db[plr][7]=scores[plr]
        scores=[sum([db[db[plr][3][i]][8] for i in range(rd+1) if db[plr][2][i]==0]) for plr in range(players)]
        for plr in range(players):
            db[plr][8]=scores[plr]
    for plr in range(players):
        db[plr][7]-=db[plr][8]

def kwc(): #Kendall-Wei combined
    global Points
    Points=False
    global db
    for plr in range(players):
        db[plr][7]=sum([db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==0])
        db[plr][8]=sum([rounds-db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==0])
    for it in range(its):
        scores=[sum([db[db[plr][3][i]][7]+db[plr][7] for i in range(rd+1) if db[plr][2][i]==1]) for plr in range(players)]
        for plr in range(players):
            db[plr][7]=scores[plr]
        scores=[sum([db[db[plr][3][i]][8]+db[plr][8] for i in range(rd+1) if db[plr][2][i]==0]) for plr in range(players)]
        for plr in range(players):
            db[plr][8]=scores[plr]
    for plr in range(players):
        db[plr][7]-=db[plr][8]

# Evaluation Function   
def Eval():
    if Points:
        actual=[i[0] for i in sorted(db, key=lambda a: (a[4],a[7],a[8],a[9]))]
    else:
        actual=[i[0] for i in sorted(db, key=lambda a: (a[7]))]
    aRanks=[actual.index(i) for i in range(players)]
    return numpy.corrcoef(tRanks,aRanks)[0,1]
    
# PLAYERBASE SETUP
def reset():
    global db
    db=[]
    for ID in range(players):
        db.append([ID, random.normalvariate(0,rtgStd), [], [], 0, [], 0, 0, 0, 0])
    # Player File: ID, rating, [rd1 result, rd2 result...], [rd1 opponent, rd2 opponent], wins, performances, average performance, TB1, TB2... 

# PAIRING ALGORITHM
def pairplay():
    global db
    temp=[]
    random.shuffle(db)
    db.sort(key=lambda a: a[7])
    while db!=[]: #players play matches, results are recorded, and players are moved to the "done" zone
        p2=1
        pA=random.normalvariate(db[0][1],1)
        pB=random.normalvariate(db[p2][1],1)
        if pA>pB:
            db[0][4]+=1
            db[0][2].append(1)
            db[p2][2].append(0)
        else:
            db[p2][4]+=1
            db[p2][2].append(1)
            db[0][2].append(0)
        db[0][3].append(db[p2][0])
        db[p2][3].append(db[0][0])
        db[0][5].append(pA)
        db[p2][5].append(pB)
        temp.append(db.pop(p2))
        temp.append(db.pop(0))
    db=sorted(temp, key=lambda a: a[0])

sys1=kwr
sys2=0
sys3=0
sys4=0
sys5=0
sys6=0
sys7=0
sys8=0
sys9=0
sys10=0


# THE TOURNAMENTS
score1=[]
if testing>1:
    score2=[]
if testing>2:
    score3=[]
if testing>3:
    score4=[]
if testing>4:
    score5=[]
if testing>5:
    score6=[]
if testing>6:
    score7=[]
if testing>7:
    score8=[]
if testing>8:
    score9=[]
if testing>9:
    score10=[]
for rounds in roundsList:
    List1=[]
    if testing>1:
        List2=[]
    if testing>2:
        List3=[]
    if testing>3:
        List4=[]
    if testing>4:
        List5=[]
    if testing>5:
        List6=[]
    if testing>6:
        List7=[]
    if testing>7:
        List8=[]
    if testing>8:
        List9=[]
    if testing>9:
        List10=[]
    for rtgStd in rtgStdList:
        bList1=[]
        if testing>1:
            bList2=[]
        if testing>2:
            bList3=[]
        if testing>3:
            bList4=[]
        if testing>4:
            bList5=[]
        if testing>5:
            bList6=[]
        if testing>6:
            bList7=[]
        if testing>7:
            bList8=[]
        if testing>8:
            bList9=[]
        if testing>9:
            bList9=[]
        for p in range(tournaments):
            reset()
            for rd in range(rounds):
                pairplay()
                kwr()
            for plr in range(players):
                db[plr][6]=sum(db[plr][5])/rounds
            target=[i[0] for i in sorted(db, key=lambda a: a[6])]
            tRanks=[target.index(i) for i in range(players)]
            sys1()
            bList1.append(Eval())
            if testing>1:
                sys2()
                bList2.append(Eval())
            if testing>2:
                sys3()
                bList3.append(Eval())
            if testing>3:
                sys4()
                bList4.append(Eval())
            if testing>4:
                sys5()
                bList5.append(Eval())
            if testing>5:
                sys6()
                bList6.append(Eval())
            if testing>6:
                sys7()
                bList7.append(Eval())
            if testing>7:
                sys8()
                bList8.append(Eval())
            if testing>8:
                sys9()
                bList9.append(Eval())
            if testing>9:
                sys10()
                bList10.append(Eval())
        List1.append(numpy.mean(bList1))
        if testing>1:
            List2.append(numpy.mean(bList2))
        if testing>2:
            List3.append(numpy.mean(bList3))
        if testing>3:
            List4.append(numpy.mean(bList4))
        if testing>4:
            List5.append(numpy.mean(bList5))
        if testing>5:
            List6.append(numpy.mean(bList6))
        if testing>6:
            List7.append(numpy.mean(bList7))
        if testing>7:
            List8.append(numpy.mean(bList8))
        if testing>8:
            List9.append(numpy.mean(bList9))
        if testing>9:
            List10.append(numpy.mean(bList10))
        print(rounds,rtgStd)
    score1.append(List1)
    if testing>1:
        score2.append(List2)
    if testing>2:
        score3.append(List3)
    if testing>3:
        score4.append(List4)
    if testing>4:
        score5.append(List5)
    if testing>5:
        score6.append(List6)
    if testing>6:
        score7.append(List7)
    if testing>7:
        score8.append(List8)
    if testing>8:
        score9.append(List9)
    if testing>9:
        score10.append(List10)
print(tabulate(score1))
if testing>1:
    print(tabulate(score2))
if testing>2:
    print(tabulate(score3))
if testing>3:
    print(tabulate(score4))
if testing>4:
    print(tabulate(score5))
if testing>5:
    print(tabulate(score6))
if testing>6:
    print(tabulate(score7))
if testing>7:
    print(tabulate(score8))
if testing>8:
    print(tabulate(score9))
if testing>9:
    print(tabulate(score10))
system('say "your program has finished"')
