from scripts.outbreak import *

##########################
# 
# how to denote variables
# -----------------------
# 
# scalar - no capitals
# vector - first letter capital, the rest small
# matrix - all letters capitals


# two key files defining the division into city parts 
# zilina_city_parts.dat - here the data about the city parts are given: color coding, name and pupolation
# zilina_map_city_parts.png - geographical division of the city, with city parts color-coded according to coding in the above file

# file with initial infected - zilina_city_parts_infected.py

n_days = 150
n_loc = 12
alpha = 1.0 # DPMZ is only 40% of the transport in Zilina
gamma = 0.07
Beta = np.zeros((n_loc,1))
R0 = 1.6
M_OD = []
coef_p = 1./16.
coef_r = 0.195
coef_d = 0.07
gamma = 1./14.
gamma_a = gamma
gamma_s = gamma
gamma_h = gamma



Sus = np.zeros((n_loc,1))
InfA = np.zeros((n_loc,1))
InfS = np.zeros((n_loc,1))
Rec = np.zeros((n_loc,1))
Hos = np.zeros((n_loc,1))
Dea = np.zeros((n_loc,1))



def init():
    mapa = MapCityParts("data/zilina_map_city_parts.png")     # dimensions: 1820 x 1624
    mapa.divide_into_city_parts("data/zilina_city_parts.dat")
    #mapa.print_city_parts()
    mapa.load_stops_to_city_parts()
#    mapa.draw_map_with_stops()
    mapa.create_OD_matrix_by_city_parts("data/zilina_OD_matrix_workdays.csv")

    # load infected
    info = np.genfromtxt("data/zilina_city_parts_infected.dat",
                       usecols=(0, 1, 2),
                       delimiter=' ')

    for i in range(0,n_loc):
        InfA[i] = int(info[i][2])
        Sus[i] = mapa.city_parts[i].get_population() - InfA[i]
        InfS[i] = 0.0
        Rec[i] = 0.0
        Hos[i] = 0.0
        Dea[i] = 0.0
        Beta[i] = gamma*R0

    names_city_parts = []
    for part in mapa.city_parts:
        names_city_parts.append(part.name)
    return(mapa.OD,names_city_parts)

def load_M_OD(): # in case we have stored the OD externally
    with open('file with csv info about OD.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
            ODline = []
            if (len(row) == 3):
                for k in range(0,len(row)):
                    ODline.append(float(row[k]))
                M_OD.append(ODline)


def update():    
    Bf_tmp = np.zeros((n_loc,1))
    Sus_tmp = np.zeros((n_loc,1))
    Dea_tmp = np.zeros((n_loc,1))
    Hos_tmp = np.zeros((n_loc,1))
    Rec_tmp = np.zeros((n_loc,1))
    InfS_tmp = np.zeros((n_loc,1))
    InfA_tmp = np.zeros((n_loc,1))

    for j in range(0,n_loc):
        frac_top = 0.0
        frac_bot = 0.0
        for k in range(0,n_loc):
            frac_top += M_OD[k][j]*InfA[k]*Beta[k]/(Sus[k] + InfA[k] + Rec[k])
            frac_bot += M_OD[k][j]   # matrix is transposed, as opposed to the article about Yerevan
        frac_top *= alpha * Sus[j]
        frac_bot += Sus[j] + InfA[j] + Rec[j]
        Bf_tmp[j] = frac_top/frac_bot

        Sus_tmp[j] = Sus[j] - Beta[j] * Sus[j]*InfA[j]/(Sus[j] + InfA[j] + Rec[j]) - Bf_tmp[j]
        InfA_tmp[j] = InfA[j] + Beta[j] * Sus[j] * (1 - coef_p) * InfA[j]/(Sus[j] + InfA[j] + Rec[j]) - gamma_a*InfA[j] + (1 - coef_p)*Bf_tmp[j]
        InfS_tmp[j] = InfS[j] + Beta[j] * Sus[j] * coef_p * (1 - coef_r) * InfA[j]/(Sus[j] + InfA[j] + Rec[j]) - gamma_s * InfS[j] + coef_p * (1 - coef_r) * Bf_tmp[j]
        Hos_tmp[j] = Hos[j] + Beta[j] * Sus[j] * coef_p * coef_r * InfA[j]/(Sus[j] + InfA[j] + Rec[j]) - gamma_h*Hos[j] + coef_p * coef_r * Bf_tmp[j]
        Rec_tmp[j] = Rec[j] + gamma_a * InfA[j] + gamma_s*InfS[j] + gamma_h*(1 - coef_d) * Hos[j]
        Dea_tmp[j] = Dea[j] + gamma_h * coef_d * Hos[j]

    for j in range(0,n_loc):
        Sus[j] = Sus_tmp[j]
        Rec[j] = Rec_tmp[j]
        Hos[j] = Hos_tmp[j]
        Dea[j] = Dea_tmp[j]
        InfA[j] = InfA_tmp[j]
        InfS[j] = InfS_tmp[j]


M_OD, names_city_parts = init()
print(names_city_parts)

days = 0

Sus_Zil = np.zeros((n_days,n_loc))
Rec_Zil = np.zeros((n_days,n_loc))
Hos_Zil = np.zeros((n_days,n_loc))
Dea_Zil = np.zeros((n_days,n_loc))
InfA_Zil = np.zeros((n_days,n_loc))
InfS_Zil = np.zeros((n_days,n_loc))

Sus_Zil_tot = np.zeros((n_days,1))
Dea_Zil_tot = np.zeros((n_days,1))
Hos_Zil_tot = np.zeros((n_days,1))
Rec_Zil_tot = np.zeros((n_days,1))
InfA_Zil_tot = np.zeros((n_days,1))
InfS_Zil_tot = np.zeros((n_days,1))

while days < n_days:
    days = days + 1
    for i in range(0,n_loc):
        Sus_Zil_tot[days - 1] += Sus[i]
        Rec_Zil_tot[days - 1] += Rec[i]
        Hos_Zil_tot[days - 1] += Hos[i]
        Dea_Zil_tot[days - 1] += Dea[i]
        InfA_Zil_tot[days - 1] += InfA[i]
        InfS_Zil_tot[days - 1] += InfS[i]
        
        Sus_Zil[days - 1,i] = Sus[i]
        Rec_Zil[days - 1,i] = Rec[i]
        Hos_Zil[days - 1,i] = Hos[i]
        Dea_Zil[days - 1,i] = Dea[i]
        InfS_Zil[days - 1,i] = InfS[i]
        InfA_Zil[days - 1,i] = InfA[i]
    update()
    

d = np.arange(0, n_days , 1)    
ylim = 8000





#-------------------------------------------------------------------grafy
for i in range(0,2):
    for j in range(0,5):
        print(5 * i + j + 1)
        p = plt.subplot(3, 5, 5 * i + j + 1)
        p.set_title(str(names_city_parts[5 * i + j]))
        p.set_ylim(0,ylim)
        plt.plot(Sus_Zil[:,5 * i + j], label = "  sus")
        plt.plot(InfA_Zil[:,5 * i + j], label = "  infA")
        plt.plot(Rec_Zil[:,5 * i + j], label = "  rec")

p = plt.subplot(3, 5, 11)
p.set_title(str(names_city_parts[10]))
p.set_ylim(0,ylim)
plt.plot(Sus_Zil[:,10], label = "  sus")
plt.plot(InfA_Zil[:,10], label = "  infA")
plt.plot(Rec_Zil[:,10], label = "  rec")

p = plt.subplot(3, 5, 12)
p.set_title(str(names_city_parts[11]))
p.set_ylim(0,ylim)
plt.plot(Sus_Zil[:,11], label = "  sus")
plt.plot(InfA_Zil[:,11], label = "  infA")
plt.plot(Rec_Zil[:,11], label = "  rec")
        
p = plt.subplot(3, 5, 13)
p.set_title("Zilina")
#p.set_ylim(0,5000)
plt.plot(Sus_Zil_tot, label = "  sus")
plt.plot(InfA_Zil_tot, label = "  infA")
plt.plot(Rec_Zil_tot, label = "  rec")




plt.legend(loc = "upper right")
plt.savefig("zilina.png")
plt.show()





























