def targetPlayoff():
    for i in range(32):
        assert db[i][0]==i
    assert len(db)==32
    NFC=[]
    AFC=[]
# Division Winners
    for div in range(0,16,4): 
        teams=[db[plr] for plr in range(div, div+4)]
        teams.sort(key=lambda teams: teams[5])
        NFC.append(teams[3])
    NFC.sort(key=lambda NFC: NFC[5], reverse=True)
    for div in range(16,32,4): 
        teams=[db[plr] for plr in range(div, div+4)]
        teams.sort(key=lambda teams: teams[5])
        AFC.append(teams[3])
    AFC.sort(key=lambda AFC: AFC[5], reverse=True)
# Wild Card
    teams=[db[plr] for plr in range(16)]
    teams.sort(key=lambda teams: teams[5])
    i=14
    while len(NFC)<6:
        if teams[i] not in NFC:
            NFC.append(teams[i])
        i-=1
    teams=[db[plr] for plr in range(16,32)]
    teams.sort(key=lambda teams: teams[5])
    i=14
    while len(AFC)<6:
        if teams[i] not in AFC:
            AFC.append(teams[i])
        i-=1
    assert len(NFC)==6, "Needs to be 6 players in playoffs (NFC, Target)"
    assert len(AFC)==6, "Needs to be 6 players in playoffs (AFC, Target)"
    return [[i[0] for i in NFC],[i[0] for i in AFC]]

def targetDraft():
    return [i[0] for i in sorted(db, key=lambda db: db[5])]

def actualPlayoff():
    for i in range(32):
        assert db[i][0]==i
    assert len(db)==32
# Division Winnners
    NFC=[]
    for division in range(0,16,4): # Determine winners
        teams=[db[plr] for plr in range(division, division+4)]
        best=max(teams, key=lambda teams: teams[6])
        Continue=[i[0] for i in teams if i[6]==best[6]]
        if len(Continue)==1:
            NFC.append(Continue[0])
        else:
            NFC.append(scoreDiff(Continue))
    NFC_=[] # Sort division winners, apply tiebreakers
    wins=16
    while len(NFC_)<4:
        Continue=[i for i in NFC if db[i][6]==wins]
        while len(Continue)>1:
            NFC_.append(scoreDiff(Continue))
            Continue.remove(NFC_[-1])
        if len(Continue)==1:
            NFC_.append(Continue[0])
        wins-=1
    AFC=[] # Determine winners
    for division in range(16,32,4): 
        teams=[db[plr] for plr in range(division, division+4)]
        best=max(teams, key=lambda teams: teams[6])
        Continue=[i[0] for i in teams if i[6]==best[6]]
        if len(Continue)==1:
            AFC.append(Continue[0])
        else:
            AFC.append(scoreDiff(Continue))
    AFC_=[] # Sort division winners, apply tiebreakers
    wins=16
    while len(AFC_)<4:
        Continue=[i for i in AFC if db[i][6]==wins]
        while len(Continue)>1:
            AFC_.append(scoreDiff(Continue))
            Continue.remove(AFC_[-1])
        if len(Continue)==1:
            AFC_.append(Continue[0])
        wins-=1
# Wild Card
    teams=[db[plr] for plr in range(16)]
    wins=16
    while len(NFC_)<6:
        Continue=[i[0] for i in teams if i[6]==wins and i[0] not in NFC_]
        if len(Continue)>1:
            NFC_.append(scoreDiff(Continue))
        if len(Continue)==1:
            NFC_.append(Continue[0])
            wins-=1
        else:
            wins-=1
    teams=[db[plr] for plr in range(16,32)]
    wins=16
    while len(AFC_)<6:
        Continue=[i[0] for i in teams if i[6]==wins and i[0] not in AFC_]
        if len(Continue)>1:
            AFC_.append(scoreDiff(Continue))
        if len(Continue)==1:
            AFC_.append(Continue[0])
            wins-=1
        else:
            wins-=1
    assert len(NFC_)==6, "Needs to be 6 players in playoffs (NFC, Actual)"
    assert len(AFC_)==6, "Needs to be 6 players in playoffs (AFC, Actual)"
    return [NFC_,AFC_]

def actualDraft():
    playoffs=actualPlayoff()
# First 20: teams not in playoffs
    order=[i[0] for i in db if i[0] not in playoffs[0] and i[0] not in playoffs[1]]
# Next 4: teams eliminated in wild card round
    play(playoffs[0][3],playoffs[0][4])
    play(playoffs[1][3],playoffs[1][4])
    play(playoffs[0][2],playoffs[0][5])
    play(playoffs[1][2],playoffs[1][5])
    if db[playoffs[0][3]][2][-1]==1:
        order.append(playoffs[0].pop(4))
    else:
        order.append(playoffs[0].pop(3))
    if db[playoffs[1][3]][2][-1]==1:
        order.append(playoffs[1].pop(4))
    else:
        order.append(playoffs[1].pop(3))
    if db[playoffs[0][2]][2][-1]==1:
        order.append(playoffs[0].pop(4)) # Team 6 now in spot 5 (team 4/5 deleted)
    else:
        order.append(playoffs[0].pop(2))
    if db[playoffs[1][2]][2][-1]==1:
        order.append(playoffs[1].pop(4))
    else:
        order.append(playoffs[1].pop(2))
# Next 4: teams eliminated in divisional rounds
    play(playoffs[0][0],playoffs[0][3])
    play(playoffs[1][0],playoffs[1][3])
    play(playoffs[0][1],playoffs[0][2])
    play(playoffs[1][1],playoffs[1][2])
    if db[playoffs[0][1]][2][-1]==1:
        order.append(playoffs[0].pop(2))
    else:
        order.append(playoffs[0].pop(1))
    if db[playoffs[1][1]][2][-1]==1:
        order.append(playoffs[1].pop(2))
    else:
        order.append(playoffs[1].pop(1))
    if db[playoffs[0][0]][2][-1]==1:
        order.append(playoffs[0].pop(2)) # Team 4 now in spot 3 (team 2/3 deleted)
    else:
        order.append(playoffs[0].pop(0))
    if db[playoffs[1][0]][2][-1]==1:
        order.append(playoffs[1].pop(2))
    else:
        order.append(playoffs[1].pop(0))
# Next 2: teams eliminated in conference championships
    play(playoffs[0][0],playoffs[0][1])
    play(playoffs[1][0],playoffs[1][1])
    if db[playoffs[0][0]][2][-1]==1:
        order.append(playoffs[0].pop(1))
    else:
        order.append(playoffs[0].pop(0))
    if db[playoffs[1][0]][2][-1]==1:
        order.append(playoffs[1].pop(1))
    else:
        order.append(playoffs[1].pop(0))
# Last: super bowl loser, then winner
    play(playoffs[0][0],playoffs[1][0])
    if db[playoffs[0][0]][2][-1]==1:
        order.append(playoffs[1].pop(0))
        order.append(playoffs[0].pop(0))
    else:
        order.append(playoffs[0].pop(0))
        order.append(playoffs[1].pop(0))
# Applying tiebreakers
    order_=[]
    for wins in range(16,-1,-1):
        tied=[order[i] for i in range(20) if db[order[i]][6]==wins]
        while len(tied)>1:
            order_.insert(0,scoreDiff(tied))
            tied.remove(order_[0])
        if len(tied)==1:
            order_.insert(0,tied[0])
    for wins in range(17,-1,-1):
        tied=[order[i] for i in range(20,24) if db[order[i]][6]==wins]
        while len(tied)>1:
            order_.insert(20,scoreDiff(tied))
            tied.remove(order_[20])
        if len(tied)==1:
            order_.insert(20,tied[0])
    for wins in range(18,-1,-1):
        tied=[order[i] for i in range(24,28) if db[order[i]][6]==wins]
        while len(tied)>1:
            order_.insert(24,scoreDiff(tied))
            tied.remove(order_[24])
        if len(tied)==1:
            order_.insert(24,tied[0])
    for wins in range(19,-1,-1):
        tied=[order[i] for i in range(28,30) if db[order[i]][6]==wins]
        while len(tied)>1:
            order_.insert(28,scoreDiff(tied))
            tied.remove(order_[28])
        if len(tied)==1:
            order_.insert(28,tied[0])
    order_.extend(order[30:32])
    return order_

def evalPlayoff():
    global playoffPct
    global playoffCorr
    target=targetPlayoff()
    actual=actualPlayoff()
    playoffPct.append(len(set(target[0])&set(actual[0]))/6)
    if set(target[0])==set(actual[0]):
        ranks=[]
        for i in range(6):
            ranks.append(actual[0].index(target[0][i]))
        playoffCorr.append(corrcoef(range(6),ranks)[0,1])
    playoffPct.append(len(set(target[1])&set(actual[1]))/6)
    if set(target[1])==set(actual[1]):
        ranks=[]
        for i in range(6):
            ranks.append(actual[1].index(target[1][i]))
        playoffCorr.append(corrcoef(range(6),ranks)[0,1])
        
def evalDraft():
    global draftCorr
    target=targetDraft()
    actual=actualDraft()
    ranks=[]
    for i in range(32):
        ranks.append(actual.index(target[i]))
    draftCorr.append(corrcoef(range(32),ranks)[0,1])

        
    differences=[]
    for i in db:
        for j in i[7]:
            differences.append(abs(j))
    score1.append(sum(differences)/len(differences))
    score2.append(std(differences))
    score3.append(std([i[6] for i in db]))
