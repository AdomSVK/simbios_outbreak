from outbreak import *

mapa = MapCityParts("data/zilina_map_city_parts.png")     # dimensions: 1820 x 1624
mapa.divide_into_city_parts("data/zilina_city_parts.dat")
mapa.print_city_parts()
mapa.load_stops_to_city_parts()
mapa.draw_map_with_stops()
mapa.create_OD_matrix_by_city_parts("data/zilina_OD_matrix_workdays.csv")
print(mapa.OD)
