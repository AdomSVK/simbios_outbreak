# adds the bus stops to the mapa piture. It drwas a circel at the location of bus stop and adds the name of the bus stop (not implemented yet)

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import matplotlib.pyplot as plt
import outbreak.bus_stop

f = open("idzastavky_suradnice_v2.txt", "r")

lines = []
for line in f:
    lines.append(line.split())
f.close()
  
bus_stops = []
for line in lines:
    id = line[0]
    latt = line[len(line) - 2]
    longit = line[len(line) - 1]
    name = ''
    for i in range(1,len(line) - 2):
        name = name + " " + line[i]
    bus_stops.append(bus_stop(id,name,latt,longit))    

try:  
    img  = Image.open("mapa_okrsky.png")  
except IOError: 
    pass


draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("arial.ttf", 30)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((400, 400),"Sample Text",font = font,fill=(0,0,0,255))
img.show()

