from scipy.integrate import quad
import math
from numpy import inf
from tabulate import tabulate

def PDF(x,u=0,s=1):
    return math.e**(-(x-u)**2/(2*s*s))/(2*s*s*math.pi)**0.5

List=[]
for STD in [.1,.2,.3,.4,.5,.75,1,1.5]:
    subList=[]
    for k in [-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5]:
       subList.append(quad(lambda x: PDF(x,0)*quad(lambda y: PDF(y,k*STD),x,inf)[0],-inf,inf)[0])
    List.append(subList)

print(tabulate(List))
