import csv
import random

def round_ans(val):
    '''
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return: Rounded number (integer)
    '''
    var_rounded = (val*2+1)//2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)

# Retrieve colours from a csv file, putting them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colours = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row
all_colours.pop(0)

round_colours = []
colour_scores = []

# Loop until we have four colours with different scores
while len(round_colours) < 4:
    potential_colour = random.choice(all_colours)

    # Colour scores are being read as a string,
    # change them to an integer to compare/when writing to score list
    if potential_colour[1] not in colour_scores:
        round_colours.append(potential_colour)

        # Make score an integer and add it to the list of scores
        colour_scores.append(potential_colour[1])

print(round_colours)
print(colour_scores)

# Find target score (median)

# Change scores to integers
int_scores = [int(x) for x in colour_scores]
int_scores.sort()

median = (int_scores[1] + int_scores[2]) / 2
print("median", median)