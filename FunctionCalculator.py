#from scipy.integrate import quad
#from numpy import arange,inf
import math

file=open("Expected Rating (Win).txt")
List=eval(file.read())
file2=open("ChanceToWin.txt")
List2=eval(file2.read())

#def PDF(x,u=0,s=1):
#    return math.e**(-(x-u)**2/(2*s*s))/(2*s*s*math.pi)**0.5

def chanceToWin(d):
    if d>=6:
        return 1
    elif d<-6:
        return 0
    else:
        d=100*(d+6)
    flr=math.floor(d)
    wt=d-flr
    return wt*List2[flr-1]+(1-wt)*List2[flr]

#def chanceToWin2(d):
#    return quad(lambda x: PDF(x)*quad(lambda y: PDF(y,d),x,inf)[0],-inf,inf)[0]

def eRating(oppRtg,won=True):
    if won:
        if oppRtg>=10:
            return 7.5
        elif oppRtg<-10:
            return 0
        else:
            index=100*(oppRtg+10)
            flr=math.floor(index)
            wt=index-flr
            return wt*List[flr-1]+(1-wt)*List[flr]
    else:
        if oppRtg>=10:
            return 0
        elif oppRtg<=-10:
            return -7.5
        else:
            index=-100*(oppRtg+10)
            ceil=math.ceil(index)
            wt=index-ceil
            return -wt*List[ceil-1]-(1-wt)*List[ceil]

#def eRatingWin(defeated):
#    return quad(lambda w: w*PDF(w,0,2)*chanceToWin(w-defeated),-10,10)[0]/quad(lambda w: PDF(w,0,2)*chanceToWin(w-defeated),-10,10)[0]

