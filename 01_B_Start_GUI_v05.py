from tkinter import *

# Prevents unwanted windows
from functools import partial


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
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = ("Arial","12")

        # List for label details (text | font | row
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