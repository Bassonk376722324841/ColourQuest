from tkinter import *

# Prevents unwanted windows
from functools import partial


class Play:
    '''
    Interface for playing the Colour Quest game
    '''

    def __init__(self, rounds):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {rounds}",
                                        font=("Arial","16","bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial","16","bold"),
                                      fg="#FFFFFF", bg="#990000",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)


    def close_play(self):
        # Reshow root (ie: choose rounds) and
        # end current game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Play(4)
    root.mainloop()