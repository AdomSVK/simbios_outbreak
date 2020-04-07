import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


        
class Zastavka:
    def __init__(self, id, name, latt, longit, x, y):
        self.id = int(id)
        self.name = str(name)
        self.latt = float(latt)
        self.longit = float(longit)
        self.x = int(x)
        self.y = int(y)
        
    def label_to_map(self,draw):
        font = ImageFont.truetype("arial.ttf", 15)
        r = 3
        draw.ellipse((self.x-r, self.y-r, self.x+r, self.y+r), fill=(0,0,0,0))
        draw.text((self.x + r, self.y - r), self.name, font = font,fill=(0,0,0,255))

        


class Stvorec:
    # v skutocnosti moze byt aj obdlznik

    def __init__(self, lavy_horny = (0,0), pravy_dolny = (0,0)):
        self.zastavky = []
        # TODO populacia sa este rozdeli na SIRD
        self.populacia = 0
        self.beta = 0
        self.lavy_horny = lavy_horny
        self.pravy_dolny = pravy_dolny

    def set_populacia(self, populacia):
        self.populacia = populacia

    def get_populacia(self):
        return self.populacia

    def set_beta(self, beta):
        self.beta = beta

    def pridaj_zastavku(self, zastavka):
        if self.pravy_dolny[0] > zastavka.x > self.lavy_horny[0] \
                and self.pravy_dolny[1] > zastavka.y > self.lavy_horny[1]:
            self.zastavky.append(zastavka)


class Mapa:
    # TODO [0,0] je v lavom hornom rohu, chceme to takto?
    # TODO stvorce chceme 1D zoznam alebo 2D tabulka?

    def __init__(self, image_file):
        try:
            img = Image.open(image_file)
        except IOError:
            pass
        self.obrazok_sirka, self.obrazok_vyska = img.size
        self.stvorce = []
        self.pocet_vodorovne = 0
        self.pocet_zvisle = 0

    def rozdel_na_stvorce(self, a=50):

        #  metoda rozdeli obrazok na stvorce so stranou a
        #  pokial strany obrazku nie su delitelne cislom a, zvysne dieliky vpravo a dolu budu obdlzniky

        self.pocet_vodorovne = int(np.ceil(self.obrazok_sirka / a))
        self.pocet_zvisle = int(np.ceil(self.obrazok_vyska / a))

        y = 0
        while y < self.obrazok_vyska:
            x = 0
            while x < self.obrazok_sirka:
                self.stvorce.append(Stvorec([x, y], [min(x + a - 1, self.obrazok_sirka - 1),
                                                     min(y + a - 1, self.obrazok_vyska - 1)]))
                x += a
            y += a

    def vypis_stvorce(self):
        for i in range(0, self.pocet_zvisle):
            for j in range(0, self.pocet_vodorovne):
                print(self.stvorce[self.pocet_vodorovne * i + j].lavy_horny,
                      self.stvorce[self.pocet_vodorovne * i + j].pravy_dolny,
                      end = ", ")
            print(" ")

def load_zastavky(filename):
    f = open(filename, "r")
    lines = []
    for line in f:
        lines.append(line.split())
  
    bus_stops = []
    for line in lines:
        id = line[0]
        latt = float(line[len(line) - 2])
        longit = float(line[len(line) - 1])
        name = ''
        for i in range(1,len(line) - 2):
            name = name + " " + line[i]
        tmp = gps_to_pixel_mapa_okrsky(latt,longit)
        x = tmp[0]
        y = tmp[1]
        bus_stops.append(Zastavka(id,name,latt,longit,x,y))
    return bus_stops


def gps_to_pixel_mapa_okrsky(latt,longit):
    # calibration points
    # x-axis: 441 = 18.70737, 1310 = 18.78205
    # y-axis: 381 = 49.2449, 1540 = 49.17981

    dx = 1310 - 441
    dxGPS = 18.78205 - 18.70737
    dy = 1540 - 381
    dyGPS = 49.17981 - 49.2449
    
    zero_xGPS = 18.70737 - 441.0*dxGPS/dx
    zero_yGPS = 49.2449 - 381.0*dyGPS/dy
    
    
    return [(longit - zero_xGPS)/dxGPS*dx, (latt - zero_yGPS)/dyGPS*dy]    
    

mapa = Mapa("mapa_okrsky.png")     # dimensions: 1820 x 1624
mapa.rozdel_na_stvorce(a = 400)
#mapa.vypis_stvorce()




list_of_stops = load_zastavky("idzastavky_suradnice_v2.txt")
print(len(list_of_stops))

try:  
    img  = Image.open("empty-mapa.png")  
except IOError: 
    pass


draw = ImageDraw.Draw(img)

for zast in list_of_stops:
    zast.label_to_map(draw)

img.show()
    



