from scipy.integrate import quad
from math import e, pi
from numpy import arange,linspace
import matplotlib.pyplot as plt

def PDF(x,u,s=0.25):
    return e**(-(x-u)**2/(2*s*s))/(2*s*s*pi)**0.5

x=linspace(0,1)
e=[quad(lambda y: abs(y-z)*PDF(y,z),0,1)[0] for z in x]
plt.plot(x,e)
plt.xlabel("x")
plt.ylabel("E[|x-y|]")
plt.show()
