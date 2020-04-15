from PIL import Image, ImageDraw, ImageFont, ImageDraw
import numpy as np
import csv

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
        img  = Image.open("data/empty-mapa.png")
    except IOError:
        pass

    draw = ImageDraw.Draw(img)

    for stop in list_of_stops:
        stop.label_to_map(draw)

    img.show()


class Stop:
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

        # draw.text((x, y),"Text",(r,g,b))
        draw.text((self.x + r, self.y - r), self.name, font = font, fill=(0,0,0,255))

    def print(self):
        print(self.name, " ", self.x, " ", self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y



class Square:
    # geometrically, this can also be a rectangle

    def __init__(self, ID, upper_left = (0,0), lower_right = (0,0)):
        self.stops = []
        # TODO divide population into SIRD groups
        self.population = 0
        self.beta = 0
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.ID = ID

    def set_population(self, population):
        self.population = population

    def get_population(self):
        return self.population

    def get_ID(self):
        return self.ID

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

    def print(self):
        print("Square ", self.ID, ":")
        print("\t upper left ", self.upper_left)
        print("\t lower right ", self.lower_right)
        print("\t stops: ")
        for stop in self.stops:
            print("\t \t", end=" ")
            stop.print()



class Map:
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
        self.OD = []   # origin-destination matrix

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

    def print_squares_with_stops(self):
        for square in self.squares:
            square.print()

    def load_stops(self, filename):
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
            for i in range(1, len(line) - 2):
                name = name + " " + line[i]
            tmp = self.gps_to_pixel_map_okrsky(latt, longit)
            x = tmp[0]
            y = tmp[1]
            bus_stops.append(Stop(id, name, latt, longit, x, y))
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
            print(square_id)
            print(len(self.squares))
            self.squares[square_id].stops.append(stop)

    def create_OD_matrix_by_squares(self, detail_matrix_csv_file_name):
        list_of_stops = self.load_stops("data/zilina_id_stops_coords.txt")
        OD_detailed = self.read_detail_matrix(detail_matrix_csv_file_name)

        # initialisation of coarse OD matrix
        self.OD = [[0 for i in range(len(self.squares))] for j in range(len(self.squares))]

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

        # TODO remove squares that do not have any inhabitants


    def read_detail_matrix(self, detail_matrix_file_name):
        with open(detail_matrix_file_name) as csv_file:
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
        for i in range(len(self.squares)):
            for j in range(len(self.squares)):
                print(self.OD[i][j], end=" ")
                total_number_of_trips += self.OD[i][j]
            print(" ")
        print("total number of trips: ", total_number_of_trips)
