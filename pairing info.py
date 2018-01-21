from numpy import arange
import FunctionCalculator as fc

array=[[abs(fc.eRating(opp)*fc.chanceToWin(rating-opp)-rating)+abs(fc.eRating(opp,0)*(1-fc.chanceToWin(rating-opp))-rating) for opp in arange(-4,4.2,.2)] for rating in arange(-4,4.2,.2)]
print(array)
