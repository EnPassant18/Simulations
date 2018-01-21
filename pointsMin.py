from math import e, pi
from numpy import inf
from scipy.integrate import quad
from scipy.special import erf

def PDF(x,u=0,s=1):
    return e**(-(x-u)**2/(2*s*s))/(2*s*s*pi)**0.5
def CDF(x,u=0,s=1):
    return 0.5*(1+erf((x-u)/(s*2**0.5)))

print(quad(lambda x: PDF(x)*quad(lambda y: PDF(y)*(CDF(y)-0.5)**2,x,inf)[0],-inf,inf)[0])
