import outbreak.Map

mapa = Map("mapa_okrsky.png")     # dimensions: 1820 x 1624
mapa.divide_into_squares(square_size = 400)
mapa.print_squares_2D()
mapa.load_stops_to_squares()
mapa.print_squares_with_stops()
mapa.create_OD_matrix_by_squares("OD_matica_nedela.csv")
mapa.print_OD_matrix_by_squares()

# list_of_stops = mapa.load_stops("idzastavky_suradnice_v2.txt")
# draw_map_with_stops(list_of_stops)
    



