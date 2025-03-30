from tkinter import *

# Prevents unwanted windows
from functools import partial

import csv
import random

class Play:
    '''
    Interface for playing the Colour Quest Game
    '''

    def __init__(self, how_many):
        self.rounds_won = IntVar()

        # Lists for stats component (range is 5 items)

        # Highest score tst data...
        # self.all_scores_list = [20, 20, 20, 16, 19]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(5)

        # Lowest score test data...
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(0)

        # Random Score test data...
        self.all_scores_list = [0, 15, 16, 0, 16]
        self.all_high_score_list = [20, 18, 18, 20, 20]
        self.rounds_won.set(3)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Arial", "16", "bold"),
                                   padx=5, pady=54)
        self.heading_label.grid(row=0)

        self.stats_label = Label(self.game_frame, font=("Arial", "14", "bold"),
                                 text="Stats", width=15, fg="#FFFFFF",
                                 bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)


    def to_stats(self):
        '''
        Retrieves everything we need to display the game/round statistics
        '''

        # IMPORTANT: retrieve number of rounds
        # wom as a number instead of 'self' container
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list,
                        self.all_high_score_list]

        Stats(self, stats_bundle)


class Stats:
    '''
    Displays stats for Colour Quest Game
    '''

    def __init__(self, partner, all_stats_info):

        # Extract information from master list
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # Sort user scores to find the high score
        user_scores.sort()

        self.stats_box = Toplevel()
