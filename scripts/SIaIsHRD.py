import sys, os, math
import matplotlib.pyplot as plt
import numpy as np

N_days = 37

N_loc = 5

S = []
Ia = []
Is = []
H = []
R = []
D = []
DeltaD = []
DeltaI = []


gamma = 1./14.
gamma_a = gamma
gamma_s = gamma
gamma_h = gamma
p = 1./16.
r = 0.195
d = 0.07
R0 = 2.1
beta = R0 * gamma_a
print("beta " + str(beta))

dataIs = [44,61,84,97,107,123,137,178,185,191,204,216,226,295,295,336,336,363,400,426,450,471,485,534,581,682,701,715,728,742,769,835,863,977,1049,1089,1161]

Ia.append(2050)
Is.append(44.0)
S.append(5500000 - Ia[0] - Is[0])
R.append(0) 
H.append(0) 
D.append(0)
DeltaD.append(0)
DeltaI.append(0) 


days = 0
while days < N_days:
    days = days + 1
    S_t = S[days - 1]
    Ia_t = Ia[days - 1]
    Is_t = Is[days - 1]
    H_t = H[days - 1]
    R_t = R[days - 1]
    D_t = D[days - 1]

    S.append(S_t - beta*S_t*Ia_t/(S_t + R_t + Ia_t)) 
    Ia.append(Ia_t + beta*S_t*(1 - p)*Ia_t/(S_t + R_t + Ia_t) - gamma_a*Ia_t) 
    Is.append(Is_t + beta*S_t*p*(1 - r)*Ia_t/(S_t + R_t + Ia_t) - gamma_s*Is_t) 
    H.append(H_t + beta*S_t*p*r*Ia_t/(S_t + R_t + Ia_t) - gamma_h*H_t) 
    R.append(R_t + gamma_a*Ia_t + gamma_s*Is_t + gamma_h*(1 - d)*H_t)
    D.append(D_t + gamma_h*d*H_t)
    

    print((Is_t + H_t)/(Ia_t + Is_t + H_t))



p = plt.subplot(1, 3, 1)
plt.plot(S, label = "  sus")
plt.plot(Ia, label = "  inf asymp")
plt.plot(R, label = " rec")
plt.legend(loc = "upper right")

p = plt.subplot(1, 3, 2)
plt.plot(Is, label = " infec sympt")
plt.plot(H, label = " hosp")
plt.plot(D, label = " deaths")
plt.legend(loc = "upper right")

p = plt.subplot(1, 3, 3)
plt.plot(Is, label = " infec sympt")
plt.plot(dataIs, label = "data Is")
plt.legend(loc = "upper right")


plt.show()


