from tkinter import *

# Prevents unwanted windows
from functools import partial

import csv
import random


# Helper functions


def round_ans(val):
    '''
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return: Rounded number (integer)
    '''
    var_rounded = (val*2+1)//2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


def get_colours():
    '''
    Retrieves colours from a csv file
    :return: list of colours where each list item has the
    colour name, associated score and foreground colour for the text
    '''

    file = open("00_colour_)list_hex_v3.csv","r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove first row
    all_colours.pop(0)

    return all_colours


def get_round_colours():
    '''
    Choose four colours from larger list ensuring that scores are each different
    :return: list of colours and score to beat (mention of scores)
    '''

    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # Loop until we have four colours with different scores
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # Colour scores are being read as a string,
        # change them to an integer to compare/when writing to score list
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)

            # Make score an integer and add it to the list of scores
            colour_scores.append(potential_colour[1])

    # Change scores to integers
    int_scores = [int(x) for x in colour_scores]

    # Get median score / target score
    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median


# Classes

class StartGame:
    '''
    Initial game interface that prompts users to
    give the amount of rounds they'd like to play
    '''

    def __init__(self):
        '''
        Gets number of rounds from user
        '''

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial","16","bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)


    def check_rounds(self):
        '''
        Checks if users have entered more than 1 round
        '''

        Play(5)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:
    '''
    Interface for playing the Colour Quest game
    '''

    def __init__(self, rounds):

        # Integers / String Variables
        self.target_score = IntVar()

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_lsit = {}

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = ("Arial","12")

        # List for label details (text | font | color | row)
        play_label_list = [["Round # of #",("Arial","16","bold"), None, 0],
                           ["Score to beat: #", body_font, "#FFF2CC", 1],
                           ["Choose a colour below, good luck.", body_font, "#D5E8D4", 2],
                           ["You chose, result", body_font, "#D5E8D4", 4]]

        play_labels_ref = []
        for item in play_label_list:
            self.new_label = Label(self.game_frame, text=item[0], font=item[1],
                                   bg=item[2], wraplength=300, justify="left")
            self.new_label.grid(row=item[3], padx=10, pady=10)

            play_labels_ref.append(self.new_label)

        # Retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1],
        self.results_label = play_labels_ref[3]

        # set up colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        # Create 4 buttons in a 2x2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial","12"),
                                        text="Colour Game",width=15)
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5,pady=5)

        # Frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons ( text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Rounds", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0 , 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None]
        ]

        # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            control_button = Button(item[0], text=item[1], bg=item[2],
                                    command=item[3], font=["Arial","16","bold"],
                                    fg="#FFFFFF", width=item[4])
            control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(control_button)

        # When interface is created, invoke new
        # round function for first rounds
        self.new_round()


    def new_round(self):
        '''
         Chooses four colours, works out median for score
         to beat. Configures with chosen colours
        '''

        # Retrieve number of rounds played, add
        # one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Get round colours and median score
        self.round_colour_list, median = get_round_colours()

        # Set target score as median (for use comparison)
        self.target_score.set(median)

        # Update heading, and score to beat labels. *Hide* results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target Score: {median}",font=("Arial","14","bold"))
        self.results_label.config(text=f"{'='*7}",bg="#F0F0F0")


    def close_play(self):
        # Reshow root (ie: choose rounds) and
        # end current game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()