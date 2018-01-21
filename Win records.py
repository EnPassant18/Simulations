#source: pro football reference (seasons 2006-2015)
from numpy import std

db=[float(line) for line in open("Win records.txt")]
print(std(db))
#std=3.09788234121
#simulated std (rating:6, perf: 9) =3.07

