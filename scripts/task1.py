from scripts.outbreak import *

mapa = Map("data/zilina_map_districts.png")     # dimensions: 1820 x 1624
mapa2 = MapCityParts("data/zilina_map_city_parts.png")
mapa.divide_into_squares(square_size = 85)
print("Divided into squares.")
# mapa.print_squares_2D()
mapa.load_stops_to_squares()
print("Stops loaded to squares.")
# mapa.load_humans_to_small_squares()
# mapa.load_humans_to_big_squares()
mapa.print_squares_with_stops_and_humans()
print("Humans loaded to squares.")
mapa.create_OD_matrix_by_squares("data/zilina_OD_matrix_sunday.csv")

print("Number of squares without humans :", mapa.get_count_of_squares_without_humans())
print("Number of squares without stops :", mapa.get_count_of_squares_without_stops())
print("Number of squares with humans and without stops :", mapa.get_count_of_squares_with_humans_without_stops())
print("Number of squares without humans and with stops :", mapa.get_count_of_squares_without_humans_with_stops())

mapa.draw_map_with_stops()
mapa.draw_grid(85)
mapa.show_map()

# mapa.print_OD_matrix_by_squares()

# list_of_stops = mapa.load_stops("data/zilina_id_stops_coords.txt")
# draw_map_with_stops(list_of_stops)