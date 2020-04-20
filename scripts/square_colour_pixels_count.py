from PIL import Image
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

mapOfZilina = Image.open("data/zilina_map_districts.png").convert('RGB')
pix = mapOfZilina.load()

startingPosition = 2  # starting position of ID in a file
colourRange = 78  # colour range from the file
RGB = 3  # number of main colours in RGB model

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

firstTypeOfGrid = np.genfromtxt('data/sqare1cm.dat',
                                dtype=None,
                                usecols=None,
                                delimiter=" ")

secondTypeOfGrid = np.genfromtxt('data/sqare3cm.dat',
                                 dtype=None,
                                 usecols=None,
                                 delimiter=" ")

# Printing information about objects/files
# print(mapOfZilina)
# print('\n', inhabitants)
# print('\n', allPixelsOfColour)
# print(firstTypeOfGrid)

TotalIDsPixelCount = []  # total pixels of different colour ID on one big square
totalSumOfInhabitantsInMap = 0
numberOfSquaresInColumn = 0
numberOfSquaresInRow = 0
summed = 0

for h in range(firstTypeOfGrid.shape[0]):
    if summed == 0:
        numberOfSquaresInColumn += 1
    if firstTypeOfGrid[h][0] == 0:
        numberOfSquaresInRow += 1
        if h != 0:
            summed = 1

sumOfInhabitantsInSquareMatrix = []
for i in range(numberOfSquaresInRow):
    row = []
    for j in range(numberOfSquaresInColumn):
        row.append(0)
    sumOfInhabitantsInSquareMatrix.append(row)

for i in range(0, colourRange):
    TotalIDsPixelCount.append(0)

g = 0
f = 0

for h in range(firstTypeOfGrid.shape[0]):  # each square in a row
    IDsPixelCount = []  # each square pixels of different colour ID

    for i in range(0, colourRange):
        IDsPixelCount.append(0)

    for i in range(firstTypeOfGrid[h][0], firstTypeOfGrid[h][2]):
        for j in range(firstTypeOfGrid[h][1], firstTypeOfGrid[h][3]):
            for k in range(0, colourRange):
                theSame = 1
                for m in range(RGB):
                    if colors[k][m] != pix[i, j][m]:
                        theSame = 0
                        break
                if theSame:
                    IDsPixelCount[k] += 1
                    TotalIDsPixelCount[k] += 1

    inhabitantsInSquare = []  # array of inhabitants in small square
    sumOfInhabitantsInSquare = 0  # sum of all inhabitants in small square

    for i in range(0, colourRange):
        inhabitantsInSquare.append(IDsPixelCount[i] / allPixelsOfColour[i] * inhabitants[i])
        sumOfInhabitantsInSquare += inhabitantsInSquare[i]

    sumOfInhabitantsInSquareMatrix[f][g] = sumOfInhabitantsInSquare
    totalSumOfInhabitantsInMap += sumOfInhabitantsInSquare

    g += 1
    if g == numberOfSquaresInColumn:
        g = 0
        f += 1

for i in range(colourRange):
    print(i + 2, " ", TotalIDsPixelCount[i])

print(pd.DataFrame(sumOfInhabitantsInSquareMatrix))

print('\n', "Total inhabitants on the map is : ", totalSumOfInhabitantsInMap)
