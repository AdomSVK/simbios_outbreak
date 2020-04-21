from outbreak import Map

mapa = Map("data/zilina_map_districts.png")     # dimensions: 1820 x 1624
mapa.divide_into_squares(square_size = 400)
mapa.print_squares_2D()
mapa.load_stops_to_squares()
mapa.print_squares_with_stops()
mapa.create_OD_matrix_by_squares("data/zilina_OD_matrix_sunday.csv")
mapa.print_OD_matrix_by_squares()

# list_of_stops = mapa.load_stops("data/zilina_id_stops_coords.txt")
# draw_map_with_stops(list_of_stops)
    



