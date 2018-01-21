from numpy import arange
from tabulate import tabulate
rj=1
array=[]
for e in arange(-2,2.2,0.2):
    List=[]
    for r in arange(-2,2.2,0.2):
        win=1/(1+10**(rj-r))*(abs(e-r)-abs(e+0.25*(1-1/(1+10**(rj-e)))-r))
        lose=1/(1+10**(r-rj))*(abs(e-r)-abs(e+0.25*(-1/(1+10**(rj-e)))-r))
        List.append(win+lose)
    array.append(List)
print(tabulate(array))
