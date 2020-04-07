# creates the list of bus_stops (there is a class bus_stop holding information about the bus stops)
import outbreak.bus_stop

f = open("idzastavky_suradnice_v2.txt", "r")

lines = []
for line in f:
    lines.append(line.split())
  
bus_stops = []
for line in lines:
    id = line[0]
    latt = line[len(line) - 2]
    longit = line[len(line) - 1]
    name = ''
    for i in range(1,len(line) - 2):
        name = name + " " + line[i]
    bus_stops.append(bus_stop(id,name,latt,longit))    

print(bus_stops[0].id, bus_stops[0].name, bus_stops[0].latt, bus_stops[0].longit)
f.close()
