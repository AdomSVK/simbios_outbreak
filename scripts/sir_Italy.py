import sys, os, math
import matplotlib.pyplot as plt
import numpy as np
from ItalyCovid import *

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

gamma = 0.036
beta = 0.3
alfa = 0.002

days = 0
while days < N_days:
    if days == 47:
        gamma = 0.02
        beta = 0.155
        #alfa = 0.018
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
plt.plot(da,i,label='infected (model)')
plt.plot(da,r,label='recovered (model)')
plt.plot(da,d,label='death (model)')
#plt.plot(da,s,da,i,da,r,da,d)

filename = 'data/ItalyCovid.csv'
recovered, infected, deaths = get_csv_data(filename)
infected = [6*inf for inf in infected]
recovered = [6*rec for rec in recovered]
plt.plot(infected,label='infected')
plt.plot(recovered,label='recovered')
plt.plot(deaths,label='death')
plt.legend()
plt.ticklabel_format(style='plain')
plt.show()