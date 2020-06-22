from scripts.outbreak import *

mapa = Map("data/zilina_map_districts.png")     # dimensions: 1820 x 1624
mapa.divide_into_squares(square_size = 85)
print("Divided into squares.")

mapa.load_stops_to_squares()
print("Stops loaded to squares.")

mapa.load_humans_to_big_squares()
print("Humans loaded to squares.")

mapa.give_population_to_nearest_squares_with_stop()

#OD matrix must be created before square manipulation -> deleting squares without population
#mapa.create_OD_matrix_by_squares("data/zilina_OD_matrix_sunday.csv")
#mapa.print_OD_matrix_by_squares()

# Need to go after population manipulation
mapa.remove_squares_without_population()

#mapa.print_squares_with_stops_and_humans()

#print("Number of squares with humans and with stops :", mapa.get_count_of_squares_with_humans_with_stops())
#print("Number of squares without humans :", mapa.get_count_of_squares_without_humans())
#print("Number of squares without stops :", mapa.get_count_of_squares_without_stops())
#print("Number of squares with humans and without stops :", mapa.get_count_of_squares_with_humans_without_stops())
#print("Number of squares without humans and with stops :", mapa.get_count_of_squares_without_humans_with_stops())

#mapa.draw_map_with_stops()
#mapa.draw_grid(85)
#mapa.save_map()
#mapa.show_map()



