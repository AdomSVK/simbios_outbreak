from PIL import Image
import numpy as np

XofTopLeft = 0
YofTopLeft = 0

XofBotRight = 1820
YofBotRight = 1624

startingPosition = 2
colourRange = 78
RGB = 3

mapOfZilina = Image.open("mapa_okrsky.png").convert('RGB')
pix = mapOfZilina.load()


data = np.genfromtxt('color-coding-okrsky.dat',
                     dtype=None,
                     usecols=(1, 2, 3),
                     delimiter=' ')

#print(data)
#print(mapOfZilina)

IDs = []
newIDs = []
newPixelColours = []

for i in range(0, colourRange):
    IDs.append(0)

for i in range(XofTopLeft, XofBotRight):
    for j in range(YofTopLeft, YofBotRight):
        for k in range(0, colourRange):
            theSame = 1
            for m in range(RGB):
                if data[k][m] != pix[i, j][m]:
                    theSame = 0
                    break
            if theSame:
                IDs[k] += 1

print('\n', "Count of pixels by colour ID :", '\n')
for i in range(0, colourRange):
    print(i+startingPosition, " ", IDs[i])


