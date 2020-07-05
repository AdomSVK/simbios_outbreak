from PIL import Image, ImageDraw, ImageFont, ImageDraw
import numpy as np
import pandas as pd
import csv
import json


import matplotlib.pyplot as plt

def pixel_to_gps_mapa_okrsky(x, y):
    # calibration points
    # x-axis: 441 = 18.70737, 1310 = 18.78205
    # y-axis: 381 = 49.2449, 1540 = 49.17981

    dx = 1310 - 441
    dxGPS = 18.78205 - 18.70737
    dy = 1540 - 381
    dyGPS = 49.17981 - 49.2449

    zero_xGPS = 18.70737 - 441 * dxGPS / dx
    zero_yGPS = 49.2449 - 381 * dyGPS / dy

    return [zero_xGPS + x * dxGPS / dx, zero_yGPS + y * dyGPS / dy]


def gps_to_pixel_mapa_okrsky(latt, longit):
    # calibration points
    # x-axis: 441 = 18.70737, 1310 = 18.78205
    # y-axis: 381 = 49.2449, 1540 = 49.17981

    dx = 1310 - 441
    dxGPS = 18.78205 - 18.70737
    dy = 1540 - 381
    dyGPS = 49.17981 - 49.2449

    zero_xGPS = 18.70737 - 441 * dxGPS / dx
    zero_yGPS = 49.2449 - 381 * dyGPS / dy

    return [(longit - zero_xGPS) / dxGPS * dx, (latt - zero_yGPS) / dyGPS * dy]
        

def draw_map_with_stops(list_of_stops):

    try:
        img  = Image.open("data/zilina_map_empty.png")
    except IOError:
        pass

    draw = ImageDraw.Draw(img)

    for stop in list_of_stops:
        stop.label_to_map(draw)

    img.show()

#parsing whole feed step by step
def parse_feed_to_parts(feed):
    #load feed from .txt file and split it into small parts containing information about one patient + create emptz array of covid cases
    registered_covid_cases = []
    f = open(feed, errors='ignore')
    big_string = f.read()
    #string_array = []
    string_array = big_string.split("},{")

    #remove '{' and '}' character from strings
    i = 0
    while i < len(string_array):
        string_array[i] = string_array[i].translate({ord(i): None for i in '{}'})
        #string_array[i] = string_array[i].replace('"', '')
        i += 1

    # help print
    #i = 0
    #while i < len(string_array):
        #print(string_array[i])
        #i += 1

    #splitting patient information to smaller parts and creating single patient from it
    i = 0
    while i < len(string_array):

        particle = string_array[i].split(',"')

        j = 0
        while j < len(particle):
            help_particle = particle[j].split('":')
            del help_particle[0]
            particle[j] = help_particle[0]
            j += 1
        try:
            patient_ordinal_number = int(particle[0].replace('"',''))
        except ValueError:
            patient_ordinal_number = 0
        covid19_suspected_at = str(particle[1])
        covid19_confirmed_positive_at = str(particle[2])
        covid19_confirmed_negative_at = str(particle[3])
        patient_recovered_at = str(particle[4])
        patient_deceased_at = str(particle[5])
        patient_sex = str(particle[6])
        patient_age = int(particle[7].replace('"',''))
        category = str(particle[8])
        patient_addressOfStay_City = str(particle[9])
        patient_addressOfStay_Street = str(particle[10])
        try:
            city_latitude = float(particle[11].replace('"',''))
        except ValueError:
            city_latitude = 0.0
        try:
            city_longitude = float(particle[12].replace('"',''))
        except:
            city_longitude = 0.0
        try:
            street_latitude = float(particle[13].replace('"',''))
        except ValueError:
            street_latitude = 0.0
        try:
            street_longitude = float(particle[14].replace('"',''))
        except ValueError:
            street_longitude = 0.0
        note = str(particle[15])
        try:
            is_public = int(particle[16].replace('"',''))
        except ValueError:
            is_public = 0

        covid_case = RegistredCovCase(patient_ordinal_number, covid19_suspected_at, covid19_confirmed_positive_at, covid19_confirmed_negative_at,
                                      patient_recovered_at, patient_deceased_at, patient_sex, patient_age, category, patient_addressOfStay_City, patient_addressOfStay_Street,
                                      city_latitude, city_longitude, street_latitude, street_longitude, note, is_public)
        registered_covid_cases.append(covid_case)
        i += 1

    #help print
    #i = 0
    #while i < len(particle):
        #print(i, particle[i])
        #i += 1
    for x in range(0, len(registered_covid_cases)):
        registered_covid_cases[x].print_info()

    return registered_covid_cases


def is_color_in_list_of_colors(color,list_colors):
    # detects, whether given color exists in the list of colors. Return 1 if it does, returns 0 if it does not.
    for col in list_colors:
        if color[0] == col[0] and color[1] == col[1] and color[2] == col[2]:
            return 1
    return 0

def extract_districts_map(filename):
    # takes the original map and creates a new file with only districts
    try:
        mapOfZilina  = Image.open(filename).convert('RGB')
    except IOError:
        pass

    w, h = mapOfZilina.size  # getting max. size of both axis
    colors = np.genfromtxt('data/zilina_color_coding_districts.dat',
                       dtype=None,
                       usecols=(1, 2, 3),
                       delimiter=' ')
    colourRange = 78
    new_image = Image.new('RGB', (w, h))
    for i in range(0, w):
        print(str(i) + "/" + str(w))
        for j in range(0, h):
            current_color = mapOfZilina.getpixel( (i,j) )
            if is_color_in_list_of_colors(current_color,colors) == 1:
                new_image.putpixel( (i,j), current_color)
            else:
                new_image.putpixel( (i,j), (255,255,255))
    new_image.save("data/zilina_map_only_districts.png")

def overlay_map_with_districts():
    # one-time function for corretcint the original map. Takes the empty map, takes the map with only districts and overlay them. 
    try:
        empty_map  = Image.open("data/zilina_map_empty.png").convert('RGB')
    except IOError:
        pass
    try:
        dist_map  = Image.open("data/zilina_map_only_districts.png").convert('RGB')
    except IOError:
        pass

    w, h = empty_map.size  # getting max. size of both axis
    for i in range(0, w):
        print(str(i) + "/" + str(w))
        for j in range(0, h):
            col = dist_map.getpixel( (i,j) )
            if col[0] != 255 or col[1] != 255 or col[2] != 255:
                empty_map.putpixel( (i,j), col)
    empty_map.save("data/zilina_map_districts_corrected.png")

class Stop:
    def __init__(self, id, id_in_list, name, latt, longit, x, y):
        self.id = int(id)
        self.id_in_list = int(id_in_list)
        #print(id_in_list)
        self.name = str(name)
        self.latt = float(latt)
        self.longit = float(longit)
        self.x = int(x)
        self.y = int(y)

    def get_name(self):
        return self.name

    def label_to_map(self,draw):
        font = ImageFont.truetype("data/arial.ttf", 15)
        r = 3
        draw.ellipse((self.x-r, self.y-r, self.x+r, self.y+r), fill=(0,0,0,0))

        # draw.text((x, y),"Text",(r,g,b))
        draw.text((self.x + r, self.y - r), self.name, font = font, fill=(0,0,0,255))

    def print(self):
        print(self.name, " ", self.x, " ", self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class RegistredCovCase:
    def __init__(self, patient_ordinal_number, covid19_suspected_at, covid19_confirmed_positive_at, covid19_confirmed_negative_at, patient_recovered_at, patient_deceased_at,
                 patient_sex, patient_age, category, patient_addressOfStay_City, patient_addressOfStay_Street, city_latitude, city_longitude, street_latitude, street_longitude,
                 note, is_public):
        self.patient_ordinal_number = int(patient_ordinal_number)
        self.covid19_suspected_at = str(covid19_suspected_at)
        self.covid19_confirmed_positive_at = str(covid19_confirmed_positive_at)
        self.covid19_confirmed_negative_at = str(covid19_confirmed_negative_at)
        self.patient_recovered_at = str(patient_recovered_at)
        self.patient_deceased_at = str(patient_deceased_at)
        self.patient_sex = str(patient_sex)
        self.patient_age = int(patient_age)
        self.category = str(category)
        self.patient_addressOfStay_City = str(patient_addressOfStay_City)
        self.patient_addressOfStay_Street = str(patient_addressOfStay_Street)
        self.city_latitude = float(city_latitude)
        self.city_longitude = float(city_longitude)
        self.street_latitude = float(street_latitude)
        self.street_longitude = float(street_longitude)
        self.note = str(note)
        self.is_public = int(is_public)

    def print_info(self):
        print("patient_ordinal_number: " + str(self.patient_ordinal_number) + " , " + "covid19_suspected_at: " + self.covid19_suspected_at + " , " + "covid19_confirmed_positive_at: " + self.covid19_confirmed_positive_at + " , " +
              "covid19_confirmed_negative_at: " + self.covid19_confirmed_negative_at + " , " + "patient_recovered_at: " + self.patient_recovered_at + " , " + "patient_deceased_at: " + self.patient_deceased_at + " , " +
              "patient_sex: " + " , " + self.patient_sex + " , " + "patient_age: " + str(self.patient_age) + " , " + "category: " + self.category + " , " + "patient_adressOfStay_City: " + self.patient_addressOfStay_City + " , " +
              "patient_adressOfStay_Street: " + self.patient_addressOfStay_Street + " , " + "city_latitude: " + str(self.city_latitude) + " , " + "city_longitude: " + str(self.city_longitude) + " , " + "street_latitude: " + str(self.street_latitude) + " , " + "street_longitude: " + str(self.street_longitude) + " , " +
              "note: " + self.note + " , " + "is_public: " + str(self.is_public))


def load_json_virus_spread():

    with open('data/SR_virus_spread_across_unicipalities_v17april_MRandMGmodel.json', errors='ignore') as f:
        data = json.load(f)

    municipalities = []

    city_names = data['city_names']
    city_sizes = data['city_sizes']
    infected = data['data']['infected']

    for x in city_names:
        insert = Municipality()
        insert.name = x
        municipalities.append(insert)

    i = 0
    for x in city_sizes:
        municipalities[i].population = x
        i += 1

    for days in infected:
        i = 0
        for city_x in days:
            municipalities[i].infected.append(city_x)
            i += 1

    return municipalities

def load_pickle_matrix(file):
    try:
        matrix = np.load(file, allow_pickle=True)
        print("Matrix succesfully loaded !")
    except IOError:
        print("Can't load this file !")
        pass
    municipality_array = []
    #1402 riadok aj stlpec je ZA

    for i in range(0, len(matrix)):                         #na riadku i a stlpci j je pocet obyvatelov, ktori sa presuvaju z mesta i do mesta j
        municipality = Municipality()
        municipality.name = str(i)
        municipality.flow_from_Zilina = matrix[1402][i]
        municipality.flow_to_Zilina = matrix[i][1402]
        municipality_array.append(municipality)

    print("Country: " + str(municipality_array[0].name) + ", flow_from_ZA: " + str(
        municipality_array[0].flow_from_Zilina) + ", flow_to_ZA: " + str(municipality_array[0].flow_to_Zilina))
    print("Country: " + str(municipality_array[1].name) + ", flow_from_ZA: " + str(
        municipality_array[1].flow_from_Zilina) + ", flow_to_ZA: " + str(municipality_array[1].flow_to_Zilina))
    print("Country: " + str(municipality_array[2].name) + ", flow_from_ZA: " + str(
        municipality_array[2].flow_from_Zilina) + ", flow_to_ZA: " + str(municipality_array[2].flow_to_Zilina))
    print("Country: " + str(municipality_array[1402].name) + ", flow_from_ZA: " + str(
        municipality_array[1402].flow_from_Zilina) + ", flow_to_ZA: " + str(municipality_array[1402].flow_to_Zilina))
    #print(np.matrix(matrix))
    print(matrix[0][0])
    print(matrix[1402][1402])
    print(matrix[0][1402])
    print(matrix[1402][0])

class Municipality:
    def __init__(self):
        self.name = ""
        # TODO divide population into SIRD groups
        self.population = -1
        self.infected = []
        self.flow_from_Zilina = -1
        self.flow_to_Zilina = -1



class Square:     #EXTRA TODO
    # geometrically, this can also be a rectangle

    def __init__(self, ID, upper_left = (0,0), lower_right = (0,0)):

        # Real data
        self.ID = ID
        self.population = 0
        self.stops = []

        # Map attributes
        self.upper_left = upper_left
        self.lower_right = lower_right

        # Model attributes
        self.pismenobeta = 1.375
        self.alpha = 4.0
        # Set/Get other atributes ?
        self.coef_p = 1. / 16.
        self.coef_r = 0.195
        self.coef_d = 0.07
        self.gamma = 1. / 14.
        self.gamma_a = self.gamma
        self.gamma_s = self.gamma
        self.gamma_h = self.gamma

        self.i_position = 0
        self.j_position = 0

        self.Sus = []
        self.InfA = []
        self.InfS = []
        self.Rec = []
        self.Hos = []
        self.Dea = []
        self.Summary = []

        #self.inicialize()#fix double inicialize 1.S

    def inicialize(self):
        self.Sus.append(self.population)
        self.InfA.append(0.0)
        self.InfS.append(0.0)
        self.Rec.append(0.0)
        self.Hos.append(0.0)
        self.Dea.append(0.0)
        self.Summary.append(
            self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.InfS[len(self.InfS) - 1] + self.Rec[
                len(self.Rec) - 1] + self.Hos[len(self.Hos) - 1] + self.Dea[len(self.Dea) - 1])

    def set_i(self, i):
        self.i_position = i

    def set_j(self, j):
        self.j_position = j

    def get_i(self):
        return self.i_position

    def get_j(self):
        return self.j_position

    def add_Sus(self, count):
        self.Sus.append(count)

    def add_InfA(self, count):
        self.InfA.append(count)

    def change_InfA(self,cislo):
        self.InfA[0] = cislo
        self.Sus[0] = self.population - cislo

    def add_InfS(self, count):
        self.InfS.append(count)

    def add_Rec(self, count):
        self.Rec.append(count)

    def add_Hos(self, count):
        self.Hos.append(count)

    def add_Dea(self, count):
        self.Dea.append(count)

    def get_at_Sus(self, position):
        return self.Sus[position]

    def get_at_InfA(self, position):
        return self.InfA[position]

    def get_at_InfS(self, position):
        return self.InfS[position]

    def get_at_Rec(self, position):
        return self.Rec[position]

    def get_at_Hos(self, position):
        return self.Hos[position]

    def get_at_Dea(self, position):
        return self.Dea[position]

    def get_Sus(self):
        return self.Sus

    def get_InfA(self):
        return self.InfA

    def get_InfS(self):
        return self.InfS

    def get_Rec(self):
        return self.Rec

    def get_Hos(self):
        return self.Hos

    def get_Dea(self):
        return self.Dea

    def get_ID(self):
        return self.ID

    def get_illSymptoms(self):
        return self.InfS[len(self.InfS)-1]

    def set_population(self, population):
        self.population = population

    def get_population(self):
        return self.population

    def get_ID(self):
        return self.ID

    def get_beta(self):
        return self.pismenobeta

    def set_parameter_beta(self, beta):
        self.beta = beta

    def add_stop(self, stop):
        if self.lower_right[0] > stop.getX() > self.upper_left[0] \
                and self.lower_right[1] > stop.getY() > self.upper_left[1]:
            self.stops.append(stop)
        else:
            print("Warning: Stop does not belong to this square.")

    def has_stop(self, stop):
        # checks if the square contains this stop
        return stop in self.stops

    def has_any_stop(self):
        if len(self.stops) == 0:
            return 0
        else:
            return 1

    def print(self):
        print("Square ", self.ID, ":")
        print("Population in square :", self.get_population())
        print("Suspectible in 150 days: ",self.Sus)
        print("Infected asymptomatic in 150 days: ",self.InfA)
        print("Infected symptomatic in 150 days: ",self.InfS)
        print("Recovered in 150 days :",self.Rec)
        print("Hospitalized in 150 days: ",self.Hos)
        print("Dead in 150 days: ",self.Dea)
        print("Summary in 150 days: ", self.Summary)
        print("\t upper left ", self.upper_left)
        print("\t lower right ", self.lower_right)
        print("\t stops: ")
        for stop in self.stops:
            print("\t \t", end=" ")
            stop.print()
        print("\t humans: ", self.population)

    def selfplot(self):
        plt.plot(self.Sus, label="  sus")
        plt.plot(self.InfS, label="  infS")
        plt.plot(self.Rec, label="  rec")

        plt.legend(loc="upper right")
        #plt.savefig("zilina.png")
        #lt.show()

    #Prirobit a prisposobit funkciu update zo skriptu city_parts.py, stvorec si sam pamata-ma samotne informacie o stave, netreba robit kompletne pole pre vsetky stvorce
    #inicialiya4n0 hodnoty pre jednotlive stavy, funkcia update sa bude volať pri posunutí sa o deň viac
    def update(self, position, matrix, squares):
        frac_top = 0.0
        frac_bot = 0.0
        for k in range(0, len(squares)):
            frac_top += matrix[k][position] * squares[k].get_InfA()[len(squares[k].get_InfA())-1]\
                       * self.pismenobeta \
                        / (squares[k].get_at_Sus(len(squares[k].get_Sus())-1) +
                           squares[k].get_at_InfA(len(squares[k].get_InfA())-1) +
                           squares[k].get_at_Rec(len(squares[k].get_Rec())-1))
            frac_bot += matrix[k][position]  # matrix is transposed, as opposed to the article about Yerevan
        frac_top *= self.alpha * self.Sus[len(self.Sus)-1]
        frac_bot += self.Sus[len(self.Sus)-1] + self.InfA[len(self.InfA)-1] + self.Rec[len(self.Rec)-1]
        Bf_tmp = frac_top / frac_bot

        self.Sus.append(
            self.Sus[len(self.Sus) - 1] - self.pismenobeta * self.Sus[len(self.Sus) - 1] * self.InfA[len(self.InfA) - 1] /
            (self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.Rec[len(self.Rec) - 1]) - Bf_tmp)#

        self.InfA.append(
            self.InfA[len(self.InfA) - 1] + self.pismenobeta * self.Sus[len(self.Sus) - 1] * (1 - self.coef_p) * self.InfA[
                len(self.InfA) - 1] /
            (self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.Rec[len(self.Rec) - 1]) - self.gamma_a *
            self.InfA[len(self.InfA) - 1] + (1 - self.coef_p) * Bf_tmp )#

        self.InfS.append(
            self.InfS[len(self.InfS) - 1] + self.pismenobeta * self.Sus[len(self.Sus) - 1] * self.coef_p * (1 - self.coef_r) *
            self.InfA[len(self.InfA) - 1] /
            (self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.Rec[len(self.Rec) - 1]) - self.gamma_s *
            self.InfS[len(self.InfS) - 1] + self.coef_p * (1 - self.coef_r) * Bf_tmp)#

        self.Hos.append(
            self.Hos[len(self.Hos) - 1] + self.pismenobeta * self.Sus[len(self.Sus) - 1] * self.coef_p * self.coef_r *
            self.InfA[len(self.InfA) - 1] /
            (self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.Rec[len(self.Rec) - 1]) - self.gamma_h *
            self.Hos[len(self.Hos) - 1] + self.coef_p * self.coef_r * Bf_tmp)#

        self.Rec.append(
            self.Rec[len(self.Rec) - 1] + self.gamma_a * self.InfA[len(self.InfA) - 1] + self.gamma_s * self.InfS[
                len(self.InfS) - 1] +
            self.gamma_h * (1 - self.coef_d) * self.Hos[len(self.Hos) - 1])

        self.Dea.append(
            self.Dea[len(self.Dea) - 1] + self.gamma_h * self.coef_d * self.Hos[len(self.Hos) - 1])
        #skontrolovat spravnost vzorcov(kontrolne sucty vo stvorcoch)
        self.Summary.append(
            self.Sus[len(self.Sus) - 1] + self.InfA[len(self.InfA) - 1] + self.InfS[len(self.InfS) - 1] + self.Rec[
                len(self.Rec) - 1] + self.Hos[len(self.Hos) - 1] + self.Dea[len(self.Dea) - 1])

class Map:       #EXTRA TODO
    # [0,0] is in upper left corner

    def __init__(self, image_file):
        try:
            img = Image.open(image_file)
            self.image = img
        except IOError:
            pass
        self.img_width, self.img_height = img.size
        self.squares = []
        self.square_size = 0
        self.rows = 0
        self.columns = 0
        self.img_temp = self.image
        self.OD = []   # origin-destination matrix
        self.OD_workday = []

    def reset_map(self):
        self.image = self.img_temp

    def draw_grid(self, pixel_step):
        # Draw some lines
        # step_count = 10
        draw = ImageDraw.Draw(self.image)
        y_start = 0
        y_end = self.img_height
        step_size = pixel_step #int(self.img_height / step_count)

        for x in range(0, self.img_width, step_size):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill="black")

        x_start = 0
        x_end = self.img_width

        for y in range(0, self.img_height, step_size):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill="black")
        del draw

    def draw_map_with_stops(self):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        draw = ImageDraw.Draw(self.image)

        for stop in list_of_stops:
            stop.label_to_map(draw)

    def get_count_of_squares_without_stops(self):
        count = 0
        for sq in self.squares:
            if sq.has_any_stop() == 0:
                count += 1
        return count

    def get_count_of_squares_without_humans(self):
        count = 0
        for sq in self.squares:
            if sq.get_population() == 0:
                count += 1
        return count

    def get_count_of_squares_with_humans_without_stops(self):
        count = 0
        for sq in self.squares:
            if sq.get_population() > 0:
                if sq.has_any_stop() == 0:
                    count += 1
        return count

    # Use this method before manipulation with squares -> removing squares without population, etc.
    # Big squares only -> 85pix
    def give_population_to_nearest_squares_with_stop(self):
        for x in range(0,len(self.squares)):
            if self.squares[x].has_any_stop() == 0 and self.squares[x].get_population() > 0.0:
                count = self.count_squares_with_stop_around_position(x,1)
                #If it was unable to find in range 1 around the square square with stop it will try range 2
                if(count >= 1):
                    self.give_population_to_squares_with_stop_in_range(x,1,count)
                else:
                    count = self.count_squares_with_stop_around_position(x, 2)
                    self.give_population_to_squares_with_stop_in_range(x, 2, count)

    def give_population_to_squares_with_stop_in_range(self, position, rangee, number_of_stops_around):
        start_check_pos = position - (22*rangee) - 1 - (rangee - 1) * 2
        end_check_pos = start_check_pos + 3 + (2 ** (rangee - 1) - 1)
        for i in range(start_check_pos, end_check_pos):
            if (i > -1 and i < len(self.squares)):
                if self.squares[i].has_any_stop() == 1:
                    self.squares[i].set_population(self.squares[i].get_population() + (
                                self.squares[position].get_population() / number_of_stops_around))

        for i in range(0, rangee):
            start_check_pos += 22
            end_check_pos += 22
            if (start_check_pos > -1 and start_check_pos < len(self.squares)):
                if (self.squares[start_check_pos].has_any_stop() == 1):
                    self.squares[start_check_pos].set_population(self.squares[start_check_pos].get_population() + (
                            self.squares[position].get_population() / number_of_stops_around))

            if (end_check_pos > -1 and end_check_pos < len(self.squares)):
                if (self.squares[end_check_pos].has_any_stop() == 1):
                    self.squares[end_check_pos].set_population(self.squares[end_check_pos].get_population() + (
                            self.squares[position].get_population() / number_of_stops_around))

        start_check_pos += 22
        end_check_pos += 22
        for i in range(start_check_pos, start_check_pos + 3 + (2 ** (rangee - 1) - 1)):
            if (i > -1 and i < len(self.squares)):
                if self.squares[i].has_any_stop() == 1:
                    self.squares[i].set_population(self.squares[i].get_population() + (
                                self.squares[position].get_population() / number_of_stops_around))

        self.squares[position].set_population(0)

    #Big squares only -> 85pix
    def count_squares_with_stop_around_position(self, position, rangee):
        count = 0
        start_check_pos = position - (22*rangee) - 1 - (rangee-1)*2
        end_check_pos = start_check_pos + 3 + (2**(rangee-1)-1)
        for i in range(start_check_pos, end_check_pos):
            if(i > -1 and i < len(self.squares)):
                if self.squares[i].has_any_stop() == 1:
                    count += 1

        for i in range(0,rangee):
            start_check_pos += 22
            end_check_pos += 22
            if (start_check_pos > -1 and start_check_pos < len(self.squares)):
                if(self.squares[start_check_pos].has_any_stop() == 1):
                    count += 1

            if (end_check_pos > -1 and end_check_pos < len(self.squares)):
                if(self.squares[end_check_pos].has_any_stop() == 1):
                    count += 1

        start_check_pos += 22
        end_check_pos += 22
        for i in range(start_check_pos,start_check_pos+3+(2 ** (rangee-1)-1)):
            if(i > -1 and i < len(self.squares)):
                if self.squares[i].has_any_stop() == 1:
                    count += 1

        return count


    def get_count_of_squares_with_humans_with_stops(self):
        count = 0
        for sq in self.squares:
            if sq.get_population() > 0:
                if sq.has_any_stop() == 1:
                    count += 1
        return count

    def get_count_of_squares_without_humans_with_stops(self):
        count = 0
        for sq in self.squares:
            if sq.get_population() == 0:
                if sq.has_any_stop() == 1:
                    count += 1
        return count

    def print_names_of_stops_without_population(self):
        count = 0
        for sq in self.squares:
            if sq.get_population() == 0:
                if sq.has_any_stop() == 1:
                    for stop in sq.stops:
                        print(stop.get_name())
        return count

    #Using Trasparency
    def color_square_stategy_max_ill(self):

        max_ill = 0

        if len(self.squares) == 0:
            raise Exception("Missing squares!")

        for x in self.squares:
            if max_ill < x.get_illSymptoms():
                max_ill = x.get_illSymptoms()

        if max_ill == 0:
            raise Exception("0 sick persons!")

        COLOR = (255, 0, 0)  # Red

        self.image = self.image.convert("RGBA")
        overlay = Image.new('RGBA', self.image.size, COLOR + (0,))
        draw = ImageDraw.Draw(overlay)

        for x in self.squares:
            TRANSPARENCY =  (x.get_illSymptoms()/max_ill) # Degree of transparency, 0-100%
            OPACITY = int(255 * TRANSPARENCY)
            draw.rectangle([(x.upper_left[0],x.upper_left[1]), (x.lower_right[0],x.lower_right[1])], fill=COLOR + (OPACITY,))

        self.image= Image.alpha_composite(self.image, overlay)
        self.image = self.image.convert("RGB")
        del draw

    #Using Transparency
    def color_square_strategy_square_max_population(self): #volba no.1
        self.reset_map()
        if len(self.squares) == 0:
            raise Exception("Missing squares!")

        COLOR = (255, 0, 0)  # Red

        self.image = self.image.convert("RGBA")
        overlay = Image.new('RGBA', self.image.size, COLOR + (0,))
        draw = ImageDraw.Draw(overlay)

        for x in self.squares:
            TRANSPARENCY =  (x.get_illSymptoms()/x.get_population()) # Degree of transparency, 0-100%
            OPACITY = int(255 * TRANSPARENCY)
            draw.rectangle([(x.upper_left[0],x.upper_left[1]), (x.lower_right[0],x.lower_right[1])], fill=COLOR + (OPACITY,))

        self.image= Image.alpha_composite(self.image, overlay)
        self.image = self.image.convert("RGB")
        del draw

    def remove_squares_without_population(self):
        remove = []
        for sq in self.squares:
            if sq.get_population() == 0.0:
                remove.append(sq)
        for sq in remove:
            self.squares.remove(sq)

    def save_map(self,name):
        mapname = "mapa_" + str(name) + ".png"
        self.image.save(mapname)

    def show_map(self):
        self.image.show()

    def divide_into_squares(self, square_size=50):
        # if the image dimensions are not multiples of square_size, the remaining areas on the left and bottom
        # are divided into rectangles

        self.columns = int(np.ceil(self.img_width / square_size))
        self.rows = int(np.ceil(self.img_height / square_size))
        self.square_size = square_size

        # when creating squares, the OD matrix is erased to prevent errors
        self.OD = []

        i = 0
        y = 0
        while y < self.img_height:
            x = 0
            while x < self.img_width:
                self.squares.append(Square(i, [x, y],
                                            [min(x + self.square_size - 1, self.img_width - 1),
                                             min(y + self.square_size - 1, self.img_height - 1)]))
                i += 1
                x += square_size
            y += square_size

    def print_squares_2D(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                print(self.squares[self.columns * i + j].upper_left,
                      self.squares[self.columns * i + j].lower_right,
                      end = ", ")
            print(" ")
            

    def print_squares_to_file(self, filename):
        outfile = open(filename, "w", errors='ignore')
        for square in self.squares:
            outfile.write(str(square.upper_left[0]) + " " + str(square.upper_left[1]) + " "
                          + str(square.lower_right[0]) + " " + str(square.lower_right[1]))
        outfile.close()

    def print_squares_with_stops_and_humans(self):
        counter = 0
        for square in self.squares:
            counter = counter + 1
            square.print()
        print(counter)

    def count_all_population(self):
        count = 0

        for x in self.squares:
            count += x.get_population()

        return count

    def load_stops(self, filename):
        f = open(filename, "r", errors='ignore')
        lines = []
        for line in f:
            lines.append(line.split())

        bus_stops = []
        ii = 0
        for line in lines:
            id = line[0]
            latt = float(line[len(line) - 2])
            longit = float(line[len(line) - 1])
            name = ''
            for i in range(1, len(line) - 2):
                name = name + " " + line[i]
            tmp = self.gps_to_pixel_map_okrsky(latt, longit)
            x = tmp[0]
            y = tmp[1]
            bus_stops.append(Stop(id, ii, name, latt, longit, x, y))
            ii = ii + 1
        return bus_stops

    def gps_to_pixel_map_okrsky(self, latt, longit):
        # calibration points
        # x-axis: 441 = 18.70737, 1310 = 18.78205
        # y-axis: 381 = 49.2449, 1540 = 49.17981

        dx = 1310 - 441
        dxGPS = 18.78205 - 18.70737
        dy = 1540 - 381
        dyGPS = 49.17981 - 49.2449

        zero_xGPS = 18.70737 - 441.0 * dxGPS / dx
        zero_yGPS = 49.2449 - 381.0 * dyGPS / dy

        return [(longit - zero_xGPS) / dxGPS * dx, (latt - zero_yGPS) / dyGPS * dy]

    def load_stops_to_squares(self):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")

        for stop in list_of_stops:
            square_id = int(stop.getY() / self.square_size) * self.columns \
                         + int(stop.getX() / self.square_size)
            #print(square_id)
            # print(len(self.squares))
            self.squares[square_id].stops.append(stop)

    def load_humans_to_small_squares(self):
        humansInSmallSquares = np.genfromtxt('data/Square1cmHumans.dat',
                dtype=None,
                usecols=None,
                delimiter=" ")

        for h in range(humansInSmallSquares.shape[0]):
            self.squares[h].set_population(humansInSmallSquares[h])

        print(len(humansInSmallSquares))
        print(len(self.squares))

    def load_humans_to_big_squares(self):
        humansInBigSquares = np.genfromtxt('data/Square3cmHumans.dat',
                dtype=None,
                usecols=None,
                delimiter=" ")

        for h in range(humansInBigSquares.shape[0]):
            self.squares[h].set_population(humansInBigSquares[h])

    def create_OD_matrix_by_squares(self, detail_matrix_csv_file_name):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        OD_detailed = self.read_detail_matrix(detail_matrix_csv_file_name)
        # initialisation of coarse OD matrix
        self.OD = [[0 for i in range(len(self.squares))] for j in range(len(self.squares))] #440x440 matrix
        i = 0
        for stop_from in list_of_stops:
            square_from = int(stop_from.getY() / self.square_size) * self.columns \
                         + int(stop_from.getX() / self.square_size)
            j = 0
            for stop_to in list_of_stops:
                if int(OD_detailed[i][j]) != 0:
                    square_to = int(stop_to.getY() / self.square_size) * self.columns \
                         + int(stop_to.getX() / self.square_size)
                    self.OD[square_from][square_to] += int(OD_detailed[i][j])
                j += 1
            i += 1

    def create_OD_workday_matrix_by_squares(self, detail_matrix_csv_file_name):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        OD_detailed = self.read_detail_matrix(detail_matrix_csv_file_name)
        # initialisation of coarse OD matrix
        self.OD_workday = [[0 for i in range(len(self.squares))] for j in range(len(self.squares))] #440x440 matrix
        i = 0
        for stop_from in list_of_stops:
            square_from = int(stop_from.getY() / self.square_size) * self.columns \
                         + int(stop_from.getX() / self.square_size)
            j = 0
            for stop_to in list_of_stops:
                if int(OD_detailed[i][j]) != 0:
                    square_to = int(stop_to.getY() / self.square_size) * self.columns \
                         + int(stop_to.getX() / self.square_size)
                    self.OD_workday[square_from][square_to] += int(OD_detailed[i][j])
                j += 1
            i += 1

    # Before square manipulation Adamove mazanie matice
    def fixOD(self):
        nemaz = []
        vymaz = []
        for x in range(0, len(self.squares)):
            vymaz.append(x)
            if (self.squares[x].has_any_stop() == 1):
                nemaz.append(x)

        x = len(nemaz) - 1

        while (x >= 0):
            vymaz.remove(vymaz[nemaz[x]])
            x = x - 1

        x = len(vymaz) - 1
        while (x >= 0):
            novaOD = []

            for i in range(0, len(self.OD)):
                if i != vymaz[x]:
                    riadok = []
                    for j in range(0, len(self.OD)):
                        if j != vymaz[x]:
                           riadok.append(self.OD[i][j])
                    novaOD.append(riadok)

            self.OD = novaOD
            x = x - 1

    def fixOD_workday(self):
        nemaz = []
        vymaz = []
        for x in range(0, len(self.squares)):
            vymaz.append(x)
            if (self.squares[x].has_any_stop() == 1):
                nemaz.append(x)

        x = len(nemaz) - 1

        while (x >= 0):
            vymaz.remove(vymaz[nemaz[x]])
            x = x - 1

        x = len(vymaz) - 1
        while (x >= 0):
            novaOD = []

            for i in range(0, len(self.OD_workday)):
                if i != vymaz[x]:
                    riadok = []
                    for j in range(0, len(self.OD_workday)):
                        if j != vymaz[x]:
                           riadok.append(self.OD_workday[i][j])
                    novaOD.append(riadok)

            self.OD_workday = novaOD
            x = x - 1

    def print_OD_matrix_by_squares_Adam(self):     #Adamova uprava printu
        total_number_of_trips = 0
        for i in range(len(self.OD)):
            #print(i, end=" ")
            for j in range(len(self.OD)):
                #print(self.OD[i][j], end=" ")
                print('{:^3}'.format(self.OD[i][j]), end=" ")
            total_number_of_trips += self.OD[i][j]
            print(" ")
        print("total number of trips: ", total_number_of_trips)

    def print_OD_workday_matrix_by_squares_Adam(self):     #Adamova uprava printu
        total_number_of_trips = 0
        for i in range(len(self.OD_workday)):
            #print(i, end=" ")
            for j in range(len(self.OD_workday)):
                #print(self.OD[i][j], end=" ")
                print('{:^3}'.format(self.OD_workday[i][j]), end=" ")
            total_number_of_trips += self.OD_workday[i][j]
            print(" ")
        print("total number of trips: ", total_number_of_trips)

    def read_detail_matrix(self, detail_matrix_file_name):
        with open(detail_matrix_file_name, errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            i = 0
            OD = []
            for row in csv_reader:
                if i > 0:
                    ODline = []
                    for k in range(1, len(row)):
                        ODline.append(row[k])
                    OD.append(ODline)
                i = i + 1
            return OD

    def print_OD_matrix_by_squares(self):
        total_number_of_trips = 0
        #print("x", end=" ")
        for i in range(len(self.OD)): #self.squares
            print(i, end= " ")
            for j in range(len(self.OD)): #self.squares
                print(j, end=" ")
                #if(self.OD[i][j]==0):
                    #print(" ", end=" ")
                    #continue
                #else:
                print('{:^3}'.format(self.OD[i][j]), end= " ")   #self.OD[i][j], end=" "
                total_number_of_trips += self.OD[i][j]
            print(" ")
        print("total number of trips: ", total_number_of_trips)
        #print(self.OD[3])
        #for i in range(len(self.OD)):
            #print(self.OD[i][10])
    def detect_zeros_collumns_and_rows(self):
        checker_collumns = 0
        checker_rows = 0

        i = 0
        j = 0
        z = 0
        border = 440

        while i != border+1 and j != border + 1:
            for x in range(i,border):
                if self.OD[i][x] != 0:
                    checker_collumns = 1
                    break


            for y in range(j,border):
                if self.OD[y][j] != 0:
                    checker_rows = 1
                    break

            if checker_collumns == 1 and checker_rows == 1:
                checker_collumns = 0
                checker_rows = 0
                z = z + 1
                print("i:",i,"j:",j, "\n")

            i = i + 1
            j = j + 1
        print("count:",z)

    def whole_detection(self):
        checker_collumns = 0
        checker_rows = 0
        counter = 0

        i = 0
        j = 0
        z = 0
        while counter < len(self.OD):
            for x in range(len(self.OD)):
                if self.OD[i][x] != 0:
                    checker_collumns = 1
                    break

            for y in range(len(self.OD)):
                if self.OD[y][j] != 0:
                    checker_rows = 1
                    break

            if checker_collumns == 1 or checker_rows == 1:
                checker_collumns = 0
                checker_rows = 0
                z = z + 1
                print("i:", i, "j:", j)
            counter = counter + 1

            i = i + 1
            #print("i:",i)
            j = j + 1
            #print("j:",j)

        print("count:", z)

    def pomocna(self):
        print("row:")
        for i in range(len(self.OD)):
            print(self.OD[17][i])

        print("column:")
        for i in range(len(self.OD)):
            print(self.OD[i][17])
        print(self.OD[17][17])

    def remove_zeros_from_OD(self):
        checker_collumns = 0
        checker_rows = 0
        condition = 0
        counter = 0
        p = 0

        i = 0
        j = 0

        while counter < len(self.OD):
            for x in range(0, len(self.OD)):
                if self.OD[i][x] != 0:
                    checker_collumns = 1
                    break

            for y in range(0, len(self.OD)):
                if self.OD[y][j] != 0:
                    checker_rows = 1
                    break

            for x in range(len(self.squares)):
                c1 = self.squares[x].ID
                pom1 = int(c1 / 22)
                pom2 = int(c1 % 22)
                if (i+p) == pom1 and (j+p) == pom2:
                    condition = 1
                    break

            if checker_collumns == 0 and checker_rows == 0 and condition == 0:
                self.OD = np.delete(self.OD, i, 0)
                self.OD = np.delete(self.OD, j, 1)
                p = p + 1
                i = 0
                j = 0
                counter = 0
            else:
                checker_collumns = 0
                checker_rows = 0
                condition = 0
                counter = counter + 1
                i = i + 1
                j = j + 1

    def remove_zeros(self):
        checker_collumns = 0
        checker_rows = 0
        counter = 0

        i = 0
        j = 0

        a = np.array([[0, 1, 0, 3],
                         [4, 5, 0, 7],
                         [0, 0, 0, 0],
                         [12, 13, 0, 15]])
        print(a)
        while counter < len(a):
            for x in range(0,len(a)):
                if a[i][x] != 0:
                    checker_collumns = 1
                    break

            for y in range(0,len(a)):
                if  a[y][j] != 0:
                    checker_rows = 1
                    break

            if checker_collumns == 0 and checker_rows == 0:
                a= np.delete(a,i,0)
                a = np.delete(a,j,1)
                i = 0
                j = 0
                counter = 0
            else:
                checker_collumns = 0
                checker_rows = 0
                counter = counter + 1
                i = i + 1
                j = j + 1
        print(a)






class MapCityParts:
    # [0,0] is in upper left corner

    def __init__(self, image_file):
        try:
            img = Image.open(image_file)
            self.image = img
        except IOError:
            pass
        self.img_width, self.img_height = img.size
        self.OD = []   # origin-destination matrix
        self.city_parts = []

    def show_map(self):
        self.image.show()



    def load_stops(self, filename):
        f = open(filename, "r", errors='ignore')
        lines = []
        for line in f:
            lines.append(line.split())

        bus_stops = []
        ii = 0
        for line in lines:
            id = line[0]
            latt = float(line[len(line) - 2])
            longit = float(line[len(line) - 1])
            name = ''
            for i in range(1, len(line) - 2):
                name = name + " " + line[i]
            tmp = self.gps_to_pixel_map_okrsky(latt, longit)
            x = tmp[0]
            y = tmp[1]
            bus_stops.append(Stop(id, ii, name, latt, longit, x, y))
            ii = ii + 1
        return bus_stops

    def gps_to_pixel_map_okrsky(self, latt, longit):
        # calibration points
        # x-axis: 441 = 18.70737, 1310 = 18.78205
        # y-axis: 381 = 49.2449, 1540 = 49.17981

        dx = 1310 - 441
        dxGPS = 18.78205 - 18.70737
        dy = 1540 - 381
        dyGPS = 49.17981 - 49.2449

        zero_xGPS = 18.70737 - 441.0 * dxGPS / dx
        zero_yGPS = 49.2449 - 381.0 * dyGPS / dy

        return [(longit - zero_xGPS) / dxGPS * dx, (latt - zero_yGPS) / dyGPS * dy]


    def divide_into_city_parts(self, color_coding_file):
        # when creating city parts, the OD matrix is erased to prevent errors
        self.OD = []
        
        info = np.genfromtxt(color_coding_file,
                       dtype=(int, int, int, int, "|S10", int),
                       usecols=(0, 1, 2, 3, 4, 5),
                       delimiter=' ')
        #print(info)
        for it in info:
            tmp_city_part = CityPart()
            tmp_city_part.set_population(int(it[5]))
            tmp_city_part.set_color([int(it[1]),int(it[2]),int(it[3])])
            tmp_city_part.set_name(it[4])
            self.city_parts.append(tmp_city_part)
            
    def load_stops_to_city_parts(self):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        img_tmp = self.image.convert('RGB')

        for stop in list_of_stops:
            stop_color = img_tmp.getpixel((stop.x,stop.y))
            for part in self.city_parts:
                if stop_color[0] == part.color[0] and stop_color[1] == part.color[1] and stop_color[2] == part.color[2]:
                    stop_color_known = 1
                    part.stops.append(stop)
            if stop.id == 1: #asanacny
                self.city_parts[9].stops.append(stop)
            if stop.id == 3: #bratislavska
                self.city_parts[6].stops.append(stop)
            if stop.id == 24:
                self.city_parts[6].stops.append(stop)
            if stop.id == 25:
                self.city_parts[6].stops.append(stop)
            if stop.id == 29:
                self.city_parts[8].stops.append(stop)
            if stop.id == 69:
                self.city_parts[2].stops.append(stop)
            if stop.id == 70:
                self.city_parts[3].stops.append(stop)
            if stop.id == 74:
                self.city_parts[6].stops.append(stop)
            if stop.id == 80:
                self.city_parts[10].stops.append(stop)
            if stop.id == 87:
                self.city_parts[4].stops.append(stop)
            if stop.id == 89:
                self.city_parts[7].stops.append(stop)
            if stop.id == 97:
                self.city_parts[6].stops.append(stop)
            if stop.id == 105:
                self.city_parts[9].stops.append(stop)
            if stop.id == 123:
                self.city_parts[8].stops.append(stop)
                # need correction
                # ASAN 1 10
                # Bratislavska 3 7
                # Hricovsk 24 7
                # Priehrada 25 7
                # Hviezdoslavova 29 9
                # Pazite 69 3
                # Pietna 70 4
                # Pod zahradkou 74 7
                # Pri celulozke 80 11
                # Raj.elektr 87 5
                # Rajecka mliekaren 89 8
                # Razc Hric 97 7
                # Sibenice 105 10
                # Zel. stanica 123 9

    def create_OD_matrix_by_city_parts(self, detail_matrix_csv_file_name):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        OD_detailed = self.read_detail_matrix(detail_matrix_csv_file_name)
        
        # initialisation of coarse OD matrix
        self.OD = [[0 for i in range(len(self.city_parts))] for j in range(len(self.city_parts))]

        for i in range(0,len(self.city_parts)):
            for j in range(0,len(self.city_parts)):
                part_from = self.city_parts[i]
                part_to = self.city_parts[j]
                travelers = 0                
                for stop_from in part_from.stops:                    
                    for stop_to in part_to.stops:
                        #print(OD_detailed[stop_from.id_in_list][stop_to.id_in_list])
                        travelers += int(OD_detailed[stop_from.id_in_list][stop_to.id_in_list])
                self.OD[i][j] = travelers

    def print_city_parts(self):
        for part in self.city_parts:
            part.print_info()   

    def read_detail_matrix(self, detail_matrix_file_name):
        with open(detail_matrix_file_name, errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            i = 0
            OD = []
            for row in csv_reader:
                if i > 0:
                    ODline = []
                    for k in range(1, len(row)):
                        ODline.append(row[k])
                    OD.append(ODline)
                i = i + 1
            return OD


    def draw_map_with_stops(self):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        draw = ImageDraw.Draw(self.image)
    
        for stop in list_of_stops:
            stop.label_to_map(draw)
    
        self.image.show()

class CityPart:
    # arbitrary geometrical part of the city
    def __init__(self):
        self.stops = []
        self.population = 0
        self.beta = 0
        self.color = []
        self.name = ""

    def set_population(self, population):
        self.population = population

    def get_population(self):
        return self.population

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_parameter_beta(self, beta):
        self.beta = beta

    def print_info(self):
        print(" name " + str(self.name) + " color " + str(self.color) + " pop " + str(self.population))
        print("stops:\n")
        for stop in self.stops:
            print(stop.name)



 
