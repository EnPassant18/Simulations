import random
from math import e
from numpy import corrcoef,arange,std
from os import system

def reset():
    global db
    db=[]
    for ID in range(32):
        db.append([ID, random.normalvariate(0,6), [], [], [], 0, 0, [], 0, []])
# Player File: ID, rating, results, opponents, performances, average performance, wins, margins of victory, rating, number of injured starters

def play(p1,p2):
    global db
    db[p1][9].append(round(random.lognormvariate(0.778,1)))
    db[p2][9].append(round(random.lognormvariate(0.778,1)))
    pA=random.normalvariate(db[p1][1],8.95)+1.5-(db[p1][9][-1])*0.25
    pB=random.normalvariate(db[p2][1],8.95)-1.5-(db[p2][9][-1])*0.25
    if round(pA)>round(pB): #p1 wins
        db[p1][6]+=1
        db[p1][2].append(1)
        db[p2][2].append(0)
    elif round(pB)>round(pA): #p2 wins
        db[p2][6]+=1
        db[p2][2].append(1)
        db[p1][2].append(0)
    else:
        db[p1][6]+=0.5
        db[p2][6]+=0.5
        db[p2][2].append(0.5)
        db[p1][2].append(0.5)
    db[p1][3].append(db[p2][0])
    db[p2][3].append(db[p1][0])
    db[p1][4].append(pA)
    db[p2][4].append(pB)
    db[p1][7].append(round(pA)-round(pB))
    db[p2][7].append(round(pB)-round(pA))

def season():
    reset()
# Divisional Games
    for p1 in range(0,32,2): # (1v2, 3v4)
        play(p1,p1+1)
        play(p1+1,p1)
    for p1 in range(0,32,4): # (1v3)
        play(p1+2,p1)
        play(p1,p1+2)
    for p1 in range(1,33,4): # (2v4)
        play(p1,p1+2)
        play(p1+2,p1)
    for p1 in range(0,32,4): # (1v4)
        play(p1,p1+3)
        play(p1+3,p1)
    for p1 in range(1,33,4): # (2v3)
        play(p1,p1+1)
        play(p1+1,p1)
# Conference Games - Division Battle (AvB, CvD)
    for div in range(4):
        for p1 in range(div*8,div*8+4):
            for p2 in range(div*8+4,div*8+8):
                if p2-p1==4 or (p2-p1)%4==2:
                    play(p1,p2)
                else:
                    play(p2,p1)
# Other Conference Games
    for div in range(0,32,16): # (AvC)
        for p1 in range(div, div+4):
            play(p1,p1+8)
    for div in range(4,36,16): # (BvD)
        for p1 in range(div, div+4):
            play(p1,p1+8)
    for div in range(0,32,16): # (AvD)
        for p1 in range(div, div+4):
            play(p1+12,p1)
    for div in range(4,36,16): # (BvC)
        for p1 in range(div, div+4):
            play(p1+4,p1)
# Cross-Conference Games (AvA, BvB, etc.)
    for div in range(0,16,4):
        for p1 in range(div,div+4):
            for p2 in range(div+16,div+20):
                if (p2-p1)%4==0 or (p2-p1)%4==2:
                    play(p1,p2)
                else:
                    play(p2,p1)
    for plr in range(32):
        db[plr][5]=sum(db[plr][4])/len(db[plr][4])

def div(players):
    assert len(set([i-i%4 for i in players]))==1, "Teams not in same division"
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    assert 1<len(players), "Not enough players"
    assert 5>len(players), "Too many players"
# Head-to-Head
    p1wins=0
    p1=players[0]
    p2wins=0
    p2=players[1]
    for j in [i for i, x in enumerate(db[p1][3]) if x==p2]:
        p1wins+=db[p1][2][j]
    players[0]=[p1wins,players[0]]
    for j in [i for i, x in enumerate(db[p2][3]) if x==p1]:
        p2wins+=db[p2][2][j]
    players[1]=[p2wins,players[1]]
    if len(players)>2:
        p3=players[2]
        for j in [i for i, x in enumerate(db[p1][3]) if x==p3]:
            p1wins+=db[p1][2][j]
        for j in [i for i, x in enumerate(db[p2][3]) if x==p3]:
            p2wins+=db[p2][2][j]
        p3wins=0
        for j in [i for i, x in enumerate(db[p3][3]) if x==p1]:
            p3wins+=db[p3][2][j]
        for j in [i for i, x in enumerate(db[p3][3]) if x==p2]:
            p3wins+=db[p3][2][j]
        players[2]=[p3wins,players[2]]
    if len(players)>3:
        p4=players[3]
        for j in [i for i, x in enumerate(db[p1][3]) if x==p4]:
            p1wins+=db[p1][2][j]
        for j in [i for i, x in enumerate(db[p2][3]) if x==p4]:
            p2wins+=db[p2][2][j]
        for j in [i for i, x in enumerate(db[p3][3]) if x==p4]:
            p3wins+=db[p3][2][j]
        p4wins=0
        for j in [i for i, x in enumerate(db[p4][3]) if x==p1]:
            p4wins+=db[p4][2][j]
        for j in [i for i, x in enumerate(db[p4][3]) if x==p2]:
            p4wins+=db[p4][2][j]
        for j in [i for i, x in enumerate(db[p4][3]) if x==p3]:
            p4wins+=db[p4][2][j]
        players[3]=[p4wins,players[3]]
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Division Record
    p1wins=0
    for i in range(6):
        p1wins+=db[p1][2][i]
    players[0][0]=p1wins
    p2wins=0
    for i in range(6):
        p1wins+=db[p2][2][i]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(6):
            p3wins+=db[p3][2][i]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(6):
            p4wins+=db[p4][2][i]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Record Against Common Opponents
    p1wins=0
    for i in [0,1,2,3,4,5,6,7,8,9,12,13,14,15]:
        p1wins+=db[p1][2][i]
    players[0][0]=p1wins
    p2wins=0
    for i in [0,1,2,3,4,5,6,7,8,9,12,13,14,15]:
        p1wins+=db[p2][2][i]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in [0,1,2,3,4,5,6,7,8,9,12,13,14,15]:
            p3wins+=db[p3][2][i]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in [0,1,2,3,4,5,6,7,8,9,12,13,14,15]:
            p4wins+=db[p4][2][i]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Conference Record
    p1wins=0
    for i in range(12):
        p1wins+=db[p1][2][i]
    players[0][0]=p1wins
    p2wins=0
    for i in range(12):
        p1wins+=db[p2][2][i]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(12):
            p3wins+=db[p3][2][i]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(12):
            p4wins+=db[p4][2][i]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Strength of Victory (Neustadtl)
    p1wins=0
    for i in range(16):
        if db[p1][2][i]==1:
            p1wins+=db[db[p1][3][i]][6]
    players[0][0]=p1wins
    p2wins=0
    for i in range(16):
        if db[p2][2][i]==1:
            p1wins+=db[db[p2][3][i]][6]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(16):
            if db[p3][2][i]==1:
                p3wins+=db[db[p3][3][i]][6]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(16):
            if db[p4][2][i]==1:
                p4wins+=db[db[p4][3][i]][6]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Strength of Schedule (Solkoff)
    p1wins=0
    for i in range(16):
        p1wins+=db[db[p1][3][i]][6]
    players[0][0]=p1wins
    p2wins=0
    for i in range(16):
        p1wins+=db[db[p2][3][i]][6]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(16):
            p3wins+=db[db[p3][3][i]][6]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(16):
            p4wins+=db[db[p4][3][i]][6]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return div(Continue)
# Random Failsafe
    return p1

def wild_card(players):
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    assert len(players)>1, "Not enough teams"
# Reduction to One Team Per Division
    divisions=[]
    for plr in players:
        divisions.append(plr-plr%4)
    Set=set(divisions)
    players=[[players[i] for i in range(len(players)) if divisions[i]==j] for j in Set]
    for i in range(len(players)):
        if len(players[i])==1:
            players[i]=players[i][0]
        else:
            players[i]=div(players[i])
    if len(players)==1:
        return players[0]    
# Head-to-Head
    p1wins=0
    p1games=0
    p1=players[0]
    p2wins=0
    p2games=0
    p2=players[1]
    for j in [i for i, x in enumerate(db[p1][3]) if x==p2]:
        p1wins+=db[p1][2][j]
        p1games+=1
    for j in [i for i, x in enumerate(db[p2][3]) if x==p1]:
        p2wins+=db[p2][2][j]
        p2games+=1
    if len(players)>2:
        p3=players[2]
        for j in [i for i, x in enumerate(db[p1][3]) if x==p3]:
            p1wins+=db[p1][2][j]
            p1games+=1
        for j in [i for i, x in enumerate(db[p2][3]) if x==p3]:
            p2wins+=db[p2][2][j]
            p2games+=1
        p3wins=0
        p3games=0
        for j in [i for i, x in enumerate(db[p3][3]) if x==p1]:
            p3wins+=db[p3][2][j]
            p3games+=1
        for j in [i for i, x in enumerate(db[p3][3]) if x==p2]:
            p3wins+=db[p3][2][j]
            p3games+=1
        players[2]=[p3wins,players[2],p3games]
    if len(players)>3:
        p4=players[3]
        for j in [i for i, x in enumerate(db[p1][3]) if x==p4]:
            p1wins+=db[p1][2][j]
            p1games+=1
        for j in [i for i, x in enumerate(db[p2][3]) if x==p4]:
            p2wins+=db[p2][2][j]
            p2games+=1
        for j in [i for i, x in enumerate(db[p3][3]) if x==p4]:
            p3wins+=db[p3][2][j]
            p3games+=1
        players[2]=[p3wins,players[2][1],p3games]
        p4wins=0
        p4games=0
        for j in [i for i, x in enumerate(db[p4][3]) if x==p1]:
            p4wins+=db[p4][2][j]
            p4games+=1
        for j in [i for i, x in enumerate(db[p4][3]) if x==p2]:
            p4wins+=db[p4][2][j]
            p4games+=1
        for j in [i for i, x in enumerate(db[p4][3]) if x==p3]:
            p4wins+=db[p4][2][j]
            p4games+=1
        players[3]=[p4wins,players[3],p4games]
    players[0]=[p1wins,players[0],p1games]
    players[1]=[p2wins,players[1],p2games]
    for plr in players:
        if plr[2]==len(players)-1:
            if plr[0]==plr[2]:
                return plr[1]
            if plr[0]==0:
                del players[players.index(plr)]
                if len(players)==1:
                    return players[0][1]
                else:
                    return wild_card([i[1] for i in players])
# Conference Record
    p1wins=0
    for i in range(12):
        p1wins+=db[p1][2][i]
    players[0][0]=p1wins
    p2wins=0
    for i in range(12):
        p1wins+=db[p2][2][i]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(12):
            p3wins+=db[p3][2][i]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(12):
            p4wins+=db[p4][2][i]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return wild_card(Continue)
# Record Against Common Opponents (Min 4)
    opponents=set(db[players[0][1]][3])
    for i in range(1,len(players)):
        opponents&=set(db[players[i][1]][3])
    if len(opponents)>3:
        for i in range(len(players)):
            players[i][0]=sum([db[players[i][1]][2][j] for j in range(16) if db[players[i][0]][3][j] in opponents])
        best=max(players, key=lambda players: players[0])
        Continue=[i[1] for i in players if i[0]==best[0]]
        if len(Continue)==1:
            return Continue[0]
        if len(Continue)<len(players):
            return wild_card(Continue)
# Strength of Victory (Neustadtl)
    p1wins=0
    for i in range(16):
        if db[p1][2][i]==1:
            p1wins+=db[db[p1][3][i]][6]
    players[0][0]=p1wins
    p2wins=0
    for i in range(16):
        if db[p2][2][i]==1:
            p1wins+=db[db[p2][3][i]][6]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(16):
            if db[p3][2][i]==1:
                p3wins+=db[db[p3][3][i]][6]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(16):
            if db[p4][2][i]==1:
                p4wins+=db[db[p4][3][i]][6]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return wild_card(Continue)
# Strength of Schedule (Solkoff)
    p1wins=0
    for i in range(16):
        p1wins+=db[db[p1][3][i]][6]
    players[0][0]=p1wins
    p2wins=0
    for i in range(16):
        p1wins+=db[db[p2][3][i]][6]
    players[1][0]=p2wins
    if len(players)>2:
        p3wins=0
        for i in range(16):
            p3wins+=db[db[p3][3][i]][6]
        players[2][0]=p3wins
    if len(players)>3:
        p4wins=0
        for i in range(16):
            p4wins+=db[db[p4][3][i]][6]
        players[3][0]=p4wins
    best=max(players, key=lambda players: players[0])
    Continue=[i[1] for i in players if i[0]==best[0]]
    if len(Continue)==1:
        return Continue[0]
    if len(Continue)<len(players):
        return wild_card(Continue)
# Random Failsafe
    return p1

def solkoff(players):
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    scores=[]
    for i in players:
        total=0
        for opp in range(16):
            total+=db[db[i][3][opp]][6]
        scores.append(total)
    best=max(scores)
    Continue=[players[i] for i in range(len(players)) if scores[i]==best]
    if len(Continue)==1:
        return Continue[0]
    else:
        return rand(Continue)

def scoreDiff(players):
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    scores=[sum(db[i][7]) for i in players]
    best=max(scores)
    Continue=[players[i] for i in range(len(players)) if scores[i]==best]
    if len(Continue)==1:
        return Continue[0]
    else:
        return rand(Continue)

def oppScoreDiff(players):
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    scores=[]
    for i in players:
        total=0
        for opp in range(16):
            total+=sum(db[db[i][3][opp]][7])
        scores.append(total)
    best=max(scores)           
    Continue=[players[i] for i in range(len(players)) if scores[i]==best]
    if len(Continue)==1:
        return Continue[0]
    else:
        return rand(Continue)

def oppSRS(players):
    assert len(set([db[i][6] for i in players]))==1, "Teams not tied"
    scores=[]
    for i in players:
        total=0
        for opp in range(16):
            total+=db[db[i][3][opp]][8]
        scores.append(total)
    best=max(scores)
    Continue=[players[i] for i in range(len(players)) if scores[i]==best]
    if len(Continue)==1:
        return Continue[0]
    else:
        return rand(Continue)

def rand(players):
    return random.choice(players)

def calcSimpleRatings():
    for i in range(32):
        db[i][8]=sum(db[i][7])/16
    for i in range(100):
        ratings=[]
        for plr in db:
            ratings.append(sum([db[plr[3][opp]][8]+plr[7][opp] for opp in range(16)])/16)
        for plr in range(32):
            db[plr][8]=ratings[plr]
        if i%10==0:
            print(db[0][8]-sum(db[0][7])/16-sum([db[db[0][3][i]][8] for i in range(16)])/16)
            
def SRS(players):
    return max(players, key=lambda a: db[a][8])
        
def Eval(tbrk):
    attempts=0
    correct=0
    for wins in arange(0,16.5,0.5):
        tied=[i[0] for i in db if i[6]==wins]
        while len(tied)>1:
            winner=tbrk(tied)
            if winner==max(tied, key=lambda a: db[a][5]):
                correct+=1
            attempts+=1
            tied.remove(winner)
    if attempts!=0:
        return correct/attempts

def evalWC():
    attempts=0
    correct=0
    for wins in arange(0,16.5,0.5):
        tied=[i[0] for i in db if i[6]==wins and i[0]<16]
        while len(tied)>1:
            winner=wild_card(tied)
            if winner==max(tied, key=lambda a: db[a][5]):
                correct+=1
            attempts+=1
            tied.remove(winner)
        tied=[i[0] for i in db if i[6]==wins and i[0]>15]
        while len(tied)>1:
            winner=wild_card(tied)
            if winner==max(tied, key=lambda a: db[a][5]):
                correct+=1
            attempts+=1
            tied.remove(winner)
    if attempts!=0:
        return correct/attempts

score1=[]
#score2=[]
#score3=[]
#score4=[]
#score5=[]
#score6=[]
#score7=[]
for s in range(1):
    season()
    calcSimpleRatings()
    score1.append(Eval(scoreDiff))
print(sum(score1)/len(score1))
#print(sum(score2)/len(score2))
#print(sum(score3)/len(score3))
#print(sum(score4)/len(score4))
#print(sum(score5)/len(score5))
#print(sum(score6)/len(score6))
#print(sum(score7)/len(score7))
system('say "your program has finished"')
