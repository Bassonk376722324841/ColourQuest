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
        intro_string = ("In each round you willl be invited to choose a colour. Your goal is"
                        "to beat the target score and win the round (and keep your points).")

        # choose_string = "Oops - Please choose a whole number that isn't zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial","16","bold"), None],
            [intro_string, ("Arial","12"), None],
            [choose_string, ("Arial","12","bold"), "009900"]
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

        self.num_rounds_entry = Entry(self.entry_area_frame)


    def check_round(self):
        pass

# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")