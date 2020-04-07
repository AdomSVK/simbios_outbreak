import numpy as np
from PIL import Image

class Zastavka:

    def __init__(self, meno, x, y):
        self.meno = meno
        self.x = x
        self.y = y


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


mapa = Mapa("mapa.png")     # dimensions: 1820 x 1624
mapa.rozdel_na_stvorce(a = 400)
mapa.vypis_stvorce()

