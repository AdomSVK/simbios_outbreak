import sys, os, math
import matplotlib.pyplot as plt
import numpy as np

N = 60461826
N_days = 69

s = []
i = []
r = []
d = []

s.append(60461825)
i.append(N - s[0]) 
r.append(0)
d.append(0)

gamma = 0.02
beta = 0.1
alfa = 0.01

days = 0
while days < N_days:
    days = days + 1
    s_t = s[days - 1]
    i_t = i[days - 1]
    r_t = r[days - 1]
    d_t = d[days - 1]
    s.append(s_t - beta*s_t*i_t/N) 
    i.append(i_t + beta*s_t*i_t/N - gamma*i_t - alfa*i_t)
    r.append(r_t + gamma*i_t)
    d.append(d_t + alfa*i_t)

da = np.arange(0, N_days + 1 , 1)
print(s_t)
#plt.plot(da,s,label='susceptible')
plt.plot(da,i,label='infected')
plt.plot(da,r,label='recovered')
plt.plot(da,d,label='death')
#plt.plot(da,s,da,i,da,r,da,d)
plt.legend()
plt.show()

