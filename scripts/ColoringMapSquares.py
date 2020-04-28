from outbreak import Map

mapa = Map("data/zilina_map_districts.png")
#mapa.draw_grid(250)
mapa.divide_into_squares(square_size = 250)
mapa.color_square_stategy_max_ill()
#mapa.color_square_strategy_square_max_population()
mapa.show_map()