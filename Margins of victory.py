from numpy import std
#source: http://www.pro-football-reference.com/boxscores/game-scores.htm
db=[[int(num) for num in line.split(",")] for line in open("Margins of victory.txt")]
differences=[sum([i[1] for i in db if i[0]==j]) for j in range(74)]
print(differences)
mean=sum([i*differences[i] for i in range(74)])/sum(differences)
print(mean)
#mean=12.35853690060747
#simulated mean (rtg:6, perf:9) =12.5
print((sum([(i-mean)**2*differences[i] for i in range(74)])/sum(differences))**(1/2))
#standard dev=9.894097489588301
#simulated mean (rtg:4, perf:9) =9.4
