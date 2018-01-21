# RANKING ALGORITHMS
# x=player number
def c(x): #Classic
    global db
    return db[x][5]
def sk(x): #Solkoff
    global db
    total=0
    for i in db[x][3]:
        total+=c(i)
    return total
def mm(x): #Modified Median
    if db[x][5]>rounds/2:
        return sk(x)-min(db[i][5] for i in db[x][3])
    elif db[x][5]<rounds/2:
        return sk(x)-max(db[i][5] for i in db[x][3])
    else:
        return sk(x)-min(db[i][5] for i in db[x][3])-max(db[i][5] for i in db[x][3])
def cu(x): #Cumulative
    return sum(accumulate(db[x][2]))
def n(x): #Neustadtl
    global db
    total=0
    for i in range(rounds):
        if db[x][2][i]==1:
            total+=db[db[x][3][i]][5]
    return total
def cuo(x): #Sum of opponents' cumulative
    global db
    total=0
    for i in db[x][3]:
        total+=cu(i)
    return total
def skw(x): #cumulative-weighted solkoff
    global db
    total=0
    for i in range(rounds):
        total+=db[db[x][3][i]][5]*(rounds-i)
    return total
def skr(x): #reverse-weighted solkoff
    global db
    total=0
    for i in range(rounds):
        total+=db[db[x][3][i]][5]*(i+1)
    return total
def repeat(x):
    global db
    total=0
    for i in db[x][3]:
        total+=db[i][8]
    return (total/rounds+2*db[x][8])*1/3
def elo(x): #Performance rating estimator
    rating=0
    for i in range(rounds):
        rating+=2*(db[x][2][i]-1/(1+10**(rating-db[db[x][3][i]][8])))/(i+1)
    return rating
def elo2(x): #Performance rating estimator
    total=0
    for i in db[x][3]:
        total+=db[i][8]
    if db[x][5]==0:
        return total/rounds-2
    elif db[x][5]==rounds:
        return total/rounds+2
    else:
        return total/rounds-log(rounds/db[x][5]-1,10)
r1=db[0][8]
r2=db[1][8]
db[0][8]+=2*(db[0][2][rd]-1/(1+10**(r2-r1)))/(rd+1)
db[1][8]+=2*(db[1][2][rd]-1/(1+10**(r1-r2)))/(rd+1)
def rank(x):
    total=0
    order=[]
    for plr in sorted(db, key=lambda a: (a[5],a[8],a[9],a[10])):
        order.append(plr[0])
    for i in range(rounds):
        total+=order.index(db[x][3][i])
    return total
def Kendall_Wei(x): #Repeated Neustadtl
    global db
    total=0
    for i in range(rounds):
        if db[x][2][i]==1:
            total+=db[db[x][3][i]][8]
    return total
def david(x):
    global db
    total=db[x][5]*2-rounds
    for i in range(rounds):
        if db[x][2][i]==0:
            total-=rounds-db[db[x][3][i]][5]
        else:
            total+=db[db[x][3][i]][5]
    return total
def mov(x):
    order=[]
    for plr in sorted(db, key=lambda a: (a[5],a[9],a[10])):
                order.append(plr[0])
    total=0
    for i in range(rounds):
        if db[x][2]==1:
            total+=c(db[x][3][i])*0.5**((order.index(x)-order.index(db[x][3][i]))/players)
        else:
            total+=c(db[x][3][i])*0.5**((order.index(db[x][3][i])-order.index(x))/players)
    return total
        
    

def mm(): #Modified Median
    global Points
    Points=True
    global db
    scores=[]
    for plr in range(players):
        if db[plr][4]>rounds/2:
            db[plr][7]=sum([db[db[plr][3][opp]][4] for opp in range(rd+1)])-min(db[i][4] for i in db[plr][3])
        elif db[plr][4]<rounds/2:
            db[plr][7]=sum([db[db[plr][3][opp]][4] for opp in range(rd+1)])-max(db[i][4] for i in db[plr][3])
        else:
            db[plr][7]=sum([db[db[plr][3][opp]][4] for opp in range(rd+1)])-min(db[i][4] for i in db[plr][3])-max(db[i][4] for i in db[plr][3])

def cu(): #Cumulative
    global Points
    Points=True
    global db
    for plr in range(players):
            db[plr][7]=sum(accumulate(db[plr][2]))

def n(): #Neustadtl
    global Points
    Points=True
    global db
    for plr in range(players):
            db[plr][7]=sum([db[db[plr][3][i]][4] for i in range(rd+1) if db[plr][2][i]==1 ])
