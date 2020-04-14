import sys, os, math
import matplotlib.pyplot as plt
import numpy as np

N = 100
N_days = 50

s = []
i = []
r = []

s.append(99)
i.append(N - s[0]) 
r.append(0) 

gamma = 0.01
beta = 0.5

days = 0
while days < N_days:
    days = days + 1
    s_t = s[days - 1]
    i_t = i[days - 1]
    r_t = r[days - 1]
    s.append(s_t - beta*s_t*i_t/N) 
    i.append(i_t + beta*s_t*i_t/N - gamma*i_t) 
    r.append(r_t + gamma*i_t)

d = np.arange(0, N_days + 1 , 1)    
print(s_t)
plt.plot(d,s,d,i,d,r)
plt.show()

