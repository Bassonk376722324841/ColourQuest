import csv
import random

# Retrieve colours from a csv file, putting them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colours = list(csv.reader(file, delimiter=","))
file.close()

print(all_colours)