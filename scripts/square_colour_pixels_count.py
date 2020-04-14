from PIL import Image
import numpy as np
import math

mapOfZilina = Image.open("data/zilina_map_districts.png").convert('RGB')
pix = mapOfZilina.load()

w, h = mapOfZilina.size  # getting max. size of both axis

XofTopLeft = 0
YofTopLeft = 0

XofBotRight = w
YofBotRight = h

startingPosition = 2  # starting position of ID in a file
colourRange = 78  # colour range from the file
RGB = 3  # number of main colours in RGB model

numberOfSquaresOnMap = 9  # has to be squared number for integer number
numberOfSquaresInRow = int(math.sqrt(numberOfSquaresOnMap))  # number of squares in a row/column

xLineOfSquare = int((XofBotRight - XofTopLeft) / numberOfSquaresInRow)  # x difference from square to square
yLineOfSquare = int((YofBotRight - YofTopLeft) / numberOfSquaresInRow)  # y difference from square to square

colors = np.genfromtxt('data/zilina_color_coding_districts.dat',
                       dtype=None,
                       usecols=(1, 2, 3),
                       delimiter=' ')

inhabitants = np.genfromtxt('data/zilina_number_inhabitants_districts.dat',
                            dtype=None,
                            usecols=[1],
                            delimiter=' ')

allPixelsOfColour = np.genfromtxt('data/zilina_number_pixels_in_districts.dat',
                                  dtype=None,
                                  usecols=[1],
                                  delimiter='   ')

# Printing information about objects{files
# print(mapOfZilina)
# print('\n', inhabitants)
# print('\n', allPixelsOfColour)

TotalIDsPixelCount = []  # total pixels of different colour ID on one big square
totalSumOfInhabitantsInMap = 0  # total inhabitants in whole one big square

for i in range(0, colourRange):
    TotalIDsPixelCount.append(0)

for h in range(numberOfSquaresInRow):  # each square in a row
    for g in range(numberOfSquaresInRow):  # each square in column

        IDsPixelCount = []  # each square pixels of different colour ID

        for i in range(0, colourRange):
            IDsPixelCount.append(0)

        for i in range(XofTopLeft + h * xLineOfSquare, h * xLineOfSquare + xLineOfSquare):
            for j in range(YofTopLeft + g * yLineOfSquare, g * yLineOfSquare + yLineOfSquare):
                for k in range(0, colourRange):
                    theSame = 1
                    for m in range(RGB):
                        if colors[k][m] != pix[i, j][m]:
                            theSame = 0
                            break
                    if theSame:
                        IDsPixelCount[k] += 1
                        TotalIDsPixelCount[k] += 1

        print('\n', "Count of pixels by colour ID :", '\n')
        for i in range(0, colourRange):
            print(i + startingPosition, " ", IDsPixelCount[i])

        inhabitantsInSquare = []  # array of inhabitants in small square
        sumOfInhabitantsInSquare = 0  # sum of all inhabitants in small square

        for i in range(0, colourRange):
            inhabitantsInSquare.append(IDsPixelCount[i] / allPixelsOfColour[i] * inhabitants[i])
            sumOfInhabitantsInSquare += inhabitantsInSquare[i]

        totalSumOfInhabitantsInMap += sumOfInhabitantsInSquare

        print('\n', "Number of inhabitants in small square is : ", int(sumOfInhabitantsInSquare))

for i in range(0, colourRange):
    print(i + startingPosition, " ", TotalIDsPixelCount[i])

print('\n', "Number of inhabitants on big square is : ", int(totalSumOfInhabitantsInMap))
