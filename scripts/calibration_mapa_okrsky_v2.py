from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def pixel_to_gps_mapa_okrsky(x,y):
    # calibration points
    # x-axis: 441 = 18.70737, 1310 = 18.78205
    # y-axis: 381 = 49.2449, 1540 = 49.17981
    
    dx = 1310 - 441
    dxGPS = 18.78205 - 18.70737
    dy = 1540 - 381
    dyGPS = 49.17981 - 49.2449
    
    zero_xGPS = 18.70737 - 441*dxGPS/dx
    zero_yGPS = 49.2449 - 381*dyGPS/dy
    
    return [zero_xGPS + x*dxGPS/dx, zero_yGPS + y*dyGPS/dy]    

def gps_to_pixel_mapa_okrsky(latt,longit):
    # calibration points
    # x-axis: 441 = 18.70737, 1310 = 18.78205
    # y-axis: 381 = 49.2449, 1540 = 49.17981

    dx = 1310 - 441
    dxGPS = 18.78205 - 18.70737
    dy = 1540 - 381
    dyGPS = 49.17981 - 49.2449
    
    zero_xGPS = 18.70737 - 441*dxGPS/dx
    zero_yGPS = 49.2449 - 381*dyGPS/dy
    
    
    return [(longit - zero_xGPS)/dxGPS*dx, (latt - zero_yGPS)/dyGPS*dy]    