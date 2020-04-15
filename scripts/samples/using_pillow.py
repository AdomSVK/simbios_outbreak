from PIL import Image
import matplotlib.pyplot as plt

try:  
    img  = Image.open("mapa.png")  
except IOError: 
    pass



rgb_img = img.convert('RGB')
pixdata = img.load()

for y in range(0,img.size[1]):
    for x in range(0,img.size[0]):
        if pixdata[x, y] == (50, 0, 0, 255):
            pixdata[x, y] = (50, 255, 255, 255)
        if pixdata[x, y] == (150, 0, 0, 255):
            pixdata[x, y] = (150, 255, 255, 255)


img.show()
