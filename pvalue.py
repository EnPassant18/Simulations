from math import factorial as f
p=0
for x in range(48,81):
   p+=f(80)/f(x)/f(80-x)/2**80
print(p)
