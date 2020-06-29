from scripts.outbreak import *

mapa = Map("data/zilina_map_districts.png")     # dimensions: 1820 x 1624
mapa.divide_into_squares(square_size = 85)
print("Divided into squares.")

mapa.load_stops_to_squares()
print("Stops loaded to squares.")

mapa.load_humans_to_big_squares()
print("Humans loaded to squares.")


mapa.give_population_to_nearest_squares_with_stop()
print("Humans separate population to nearest squares.")

#OD matrix must be created before square manipulation -> deleting squares without population
mapa.create_OD_matrix_by_squares("data/zilina_OD_matrix_sunday.csv")
mapa.create_OD_workday_matrix_by_squares("data/zilina_OD_matrix_workdays.csv")
print("Matrix created.")

#mapa.print_OD_matrix_by_squares()
#print("Matrix printed.")

#mapa.detect_zeros_collumns_and_rows()
print("x")
#mapa.whole_detection()
mapa.fixOD()
mapa.fixOD_workday()
print("x")
#mapa.draw_grid(85)
#mapa.show_map()
# Need to go after population manipulation
mapa.remove_squares_without_population()
#print("Squares with no humans removed.")
#mapa.remove_zeros_from_OD()
#print("Example")
#mapa.print_OD_matrix_by_squares()
#print("matrix_sunday")
#mapa.print_OD_matrix_by_squares_Adam()
#print("matrix_workday")
#mapa.print_OD_workday_matrix_by_squares_Adam()
day = 0
for i in range(len(mapa.squares)):
    mapa.squares[i].inicialize()
mapa.squares[28].change_InfA(50.0)
while day < 150:
    for i in range(0, 77):
        mapa.squares[i].update(i, mapa.OD, mapa.squares)
    #mapa.draw_map_with_stops()
    #mapa.draw_grid(85)
    #mapa.color_square_strategy_square_max_population()
    #mapa.save_map(day)
    day = day + 1

for i in range(len(mapa.squares)):
    #print(i)
    mapa.squares[i].print()
    #mapa.squares[i].selfplot()
    #zafarbenie mapy podla udajov
    #mapa.color_square_strategy_square_max_population()
    #mapa.show_map()
#mapa.print_squares_with_stops_and_humans()
#mapa.pomocna()
#print("Advanced matrix printed.")
#print("Number of squares with humans and with stops :", mapa.get_count_of_squares_with_humans_with_stops())
#print("Number of squares without humans :", mapa.get_count_of_squares_without_humans())
#print("Number of squares without stops :", mapa.get_count_of_squares_without_stops())
#print("Number of squares with humans and without stops :", mapa.get_count_of_squares_with_humans_without_stops())
#print("Number of squares without humans and with stops :", mapa.get_count_of_squares_without_humans_with_stops())

#mapa.draw_map_with_stops()
#mapa.draw_grid(85)
#mapa.save_map()
#mapa.show_map()



