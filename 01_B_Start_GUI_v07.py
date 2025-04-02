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

    file = open("00_colour_list_hex_v3.csv","r")
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

    highest = int_scores[-1]

    return round_colours, median, highest


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

        # Strings for labels
        intro_string = ("In each round you will be invited to choose a colour. Your goal is"
                        "to beat the target score and win the round (and keep your points).")

        # choose_string = "Oops - Please choose a whole number that isn't zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial","16","bold"), None],
            [intro_string, ("Arial","12"), None],
            [choose_string, ("Arial","12","bold"), "#009900"]
        ]

        # Create labels and add them to the reference list
        start_label_ref = []

        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=350, justify="left",padx=20,pady=10)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be
        # replaced with an error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial","16","bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to homr screen)
        self.choose_label.config(fg="#889988", font=("Arial","12","bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # Checks if the amount to be converted is a number above absolute zero.
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Clear entry box and reset instruction label so that when
                # users play a new game, they don't see an error message.
                self.num_rounds_entry.delete(0,END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # Invoke Play class (and take across number of rounds)
                Play(rounds_wanted)

                # Hide root window (ie: hide rounds rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial","10","bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0,END)


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

        self.rounds_won = IntVar()

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []
        self.all_high_score_list = []

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
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_buttons_list = []
        self.colour_button_ref = []

        # Create 4 buttons in a 2x2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial","12"),
                                        text="Colour Game",width=15,
                                        command=partial(self.round_results, item))
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5,pady=5)

            self.colour_button_ref.append(self.colour_button)

        # Frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons ( text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0 , 0],
            [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 10, 0, 1],
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

        # Retrieve next, stats and end button
        # so that they can be configured
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.stats_button.config(state=DISABLED)

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
        self.round_colour_list, median, highest = get_round_colours()

        # Set target score as median (for use comparison)
        self.target_score.set(median)

        # Add median and high score to lists for stats
        self.all_medians_list.append(median)
        self.all_high_score_list.append(highest)

        # Update heading, and score to beat labels. *Hide* results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target Score: {median}", font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'='*7}", bg="#F0F0F0")

        # Configure buttons using foreground and background colours from
        # list, enable colour buttons (disabled: end of previous round)
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2],
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        '''
        Retrieves which button was pushed (index: 0-3), retrieves
        score and then compares it with median, updates results
        and adds the results to stats list
        '''

        # Enable stats button after at least one round has been played
        self.stats_button.config(state=NORMAL)

        # Get user score and colour based on button press...
        score = int(self.round_colour_list[user_choice][1])

        # Alternate way to get button name, good for if buttons have been scrambled.
        colour_name = self.colour_button_ref[user_choice].cget("text")

        # Retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)

        else:
            result_text = f"Oops, {colour_name} ({score}) is less than the target."
            result_bg = "#FBCECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # Enable stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Checks to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config()

    def close_play(self):
        # Reshow root (ie: choose rounds) and
        # end current game to start
        root.deiconify()
        self.play_box.destroy()

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
            comment_colour = "#F0F0F0"

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

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=0, padx=10, pady=10)

        # Closes help dialogue (used by button and X at top of dialogue)

    def close_stats(self, partner):
        # Put help button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()