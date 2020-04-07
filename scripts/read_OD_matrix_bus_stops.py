import csv



with open('../sources/OD_matica_nedela.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    OD = []
    for row in csv_reader:
        if i > 0:
            ODline = []
            for k in range(1,len(row)):
                ODline.append(row[k])
            OD.append(ODline)
        i = i + 1
    n_stops = i - 1
    print(OD)
