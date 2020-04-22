import csv
import matplotlib.pyplot as plt


def get_csv_data(filename):
    recovered = []
    infected = []
    deaths = []

    with open(filename, newline='') as csv_file:
        covid_reader = csv.reader(csv_file, delimiter=',')
        n_row = 0
        for row in covid_reader:
            counts = []
            for column in range(3,len(row)):
                counts.append(int(row[column]))
            if n_row == 0:
                infected = counts
            elif n_row == 1:
                recovered = counts
            elif n_row == 2:
                deaths = counts
            n_row += 1

    return recovered, infected, deaths

