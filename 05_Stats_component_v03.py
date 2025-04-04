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

        # Disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press X at top, closes
        # help and 'releases' help button
        self.stats_box.protocol("WM_DELETE_WINDOW",
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        # Math to populate stats dialogue
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # Strings for stats labels
        success_string = (f"Success Rate: {rounds_won}/{rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Possible Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

        # Custom comment text and formatting
        if total_score == max_possible:
            comment_string = ("Amazing! You got the highest"
                              "possible score!")
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = ("Oops - You've lsot every round! "
                              "You might want to look at the hints!")
            comment_colour = "#F8CECC"
            best_score_string = f"Best score: n/a"
        else:
            comment_string = ""
            comment_colour = "F0F0F0"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | font | sticky)
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)