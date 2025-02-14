"""
COMP.CS.100 Programming 1
Name: Ville Nousiainen
Student ID: 150265575
Email: ville.nousiainen2@gmail.com

A simplified game of Farkle from the video game Kingdom Come Deliverance
"""

from tkinter import *
import random
import time


"""
RULES OF THE GAME:
Farkle is a dice game with 6 dices. Goal of the game is to acquire 5000 points
with a point system. The amount of points each dice, or combination of dices 
gives is listed in the dictionary 'POINTS'. For example, "four of a kind:5" 
means there are four dices with the number 5 on each of them, and this 
equates to 1000 points.

The game starts with player 1 throwing. If there are no new points attainable 
after a throw, it's called a bust, and the turn is automatically transferred 
to the other player without adding any points to the gathered amount.

If there are points attainable, player will set aside a combination which 
gives (hopefully) the most amount of points. Now the player has a choice to 
'cash in' (Score and pass) these points to the gathered amount in the top right 
corner and forfeit the turn to the opponent. The player can also throw the 
remaining dices (which were not set aside) and attempt to get more points 
this round, with the additional risk of getting a bust. If at this moment 
there is a bust (no NEW attainable points), no points are attained from this 
round. If the player however can get more points, he can choose them and 
then is forced to turn over the turn.

This game inherently holds 2 playing styles, playing it safe and cashing in 
little amounts of points, or 'go big or go home'.

Examples of points:
[1 1 1 1 5 6] = Four of a kind of ones = 2000 + singular five = 50, 
total = 2050 points.

[2 2 2 4 4 4] = Three of a kind of twos = 200 + three of a kind of fours = 400,
total = 600 points

[1 4 3 6 5 1] = Two of singular ones = 2 * 100 points + singular five = 50, 
total = 250 points
"""


POINTS = {"five": 50, "one": 100,
          "three of a kind:1": 1000, "three of a kind:2": 200,
          "three of a kind:3": 300, "three of a kind:4": 400,
          "three of a kind:5": 500, "three of a kind:6": 600,
          "four of a kind:1": 2000, "four of a kind:2": 400,
          "four of a kind:3": 600, "four of a kind:4": 800,
          "four of a kind:5": 1000, "four of a kind:6": 1200,
          "five of a kind:1": 4000, "five of a kind:2": 800,
          "five of a kind:3": 1200, "five of a kind:4": 1600,
          "five of a kind:5": 2000, "five of a kind:6": 2400,
          "six of a kind:1": 8000, "six of a kind:2": 1600,
          "six of a kind:3": 2400, "six of a kind:4": 3200,
          "six of a kind:5": 4000, "six of a kind:6": 4800,
          "full straight": 1500, "partial straight 1-5": 500,
          "partial straight 2-6": 750}

DICES_THROWN = []
DICES_SET_ASIDE_THIS_ROUND = []

class GUI:

    def __init__(self):
        self.__main_window = Tk()

        self.__main_window.title("Farkle")
        self.__main_window.option_add("*Font", "Verdana 20")

        """Saving the regular pictures of dice in a list"""
        self.__dice_images = []
        for image_file in ["dice_1.png", "dice_2.png", "dice_3.png",
                           "dice_4.png", "dice_5.png", "dice_6.png"]:
            new_image = PhotoImage(file=image_file)
            self.__dice_images.append(new_image)

        self.__empty_image = PhotoImage(width=86, height=86)

        self.__divider = PhotoImage(file="divider.png")
        self.__thrownumber = 0

        """Instructions on the first row"""
        self.__instructions_text = Label(self.__main_window,
                                         text="Instructions: ")
        self.__instructions_text.grid(row=0, column=0, columnspan=2)

        self.__instructions_label = Label(self.__main_window)
        self.__instructions_label.grid(row=0, column=2, columnspan=8)

        """Buttons to the left side"""
        self.__throw_button = Button(self.__main_window,
                                     text="Throw",
                                     command=self.throw)
        self.__score_and_roll_again = Button(self.__main_window,
                                         text="Score and roll again",
                                         command=self.score_and_roll_again,
                                         state=DISABLED)
        self.__score_and_pass_button = Button(self.__main_window,
                                        text="Score and pass",
                                        command=self.hand_over,
                                        state=DISABLED)
        self.__new_game_button = Button(self.__main_window,
                                        text="New game",
                                        command=self.new_game)
        Button(self.__main_window, text="Quit",
               command=self.__main_window.destroy).grid(row=5, column=0,
                                                        columnspan=2,
                                                        sticky=W+E)

        self.__throw_button.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.__score_and_roll_again.grid(row=2, column=0, columnspan=2,
                                         sticky=W+E)
        self.__score_and_pass_button.grid(row=3, column=0, columnspan=2,
                                          sticky=W+E)
        self.__new_game_button.grid(row=4, column=0, columnspan=2, sticky=W+E)

        """dice view for the beginning"""
        self.__dice1button = Button(self.__main_window,
                                  image=self.__dice_images[0],
                                    command=self.move_dice1, state=DISABLED)
        self.__dice2button = Button(self.__main_window,
                                    image=self.__dice_images[1],
                                    command=self.move_dice2, state=DISABLED)
        self.__dice3button = Button(self.__main_window,
                                    image=self.__dice_images[2],
                                    command=self.move_dice3, state=DISABLED)
        self.__dice4button = Button(self.__main_window,
                                    image=self.__dice_images[3],
                                    command=self.move_dice4, state=DISABLED)
        self.__dice5button = Button(self.__main_window,
                                    image=self.__dice_images[4],
                                    command=self.move_dice5, state=DISABLED)
        self.__dice6button = Button(self.__main_window,
                                    image=self.__dice_images[5],
                                    command=self.move_dice6, state=DISABLED)
        self.__dice1button.grid(row=1, column=2, rowspan=2, columnspan=2,
                                padx=20, pady=10)
        self.__dice2button.grid(row=1, column=4, rowspan=2, columnspan=2,
                                padx=20, pady=10)
        self.__dice3button.grid(row=1, column=6, rowspan=2, columnspan=2,
                                padx=20, pady=10)
        self.__dice4button.grid(row=3, column=2, rowspan=2, columnspan=2,
                                padx=20, pady=10)
        self.__dice5button.grid(row=3, column=4, rowspan=2, columnspan=2,
                                padx=20, pady=10)
        self.__dice6button.grid(row=3, column=6, rowspan=2, columnspan=2,
                                padx=20, pady=10)

        self.__divider_label = Label(self.__main_window, image=self.__divider)
        self.__divider_label.grid(row=6, column=0, columnspan=11, sticky=W + E)

        self.__set_aside_label = Label(self.__main_window,
                                       text="Dices set aside:")
        self.__set_aside_label.grid(row=7, column=0, columnspan=2)

        """Dices for the bottom area, empty in the beginning"""
        self.__dice1button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice1_back,
                                          state=DISABLED)
        self.__dice2button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice2_back,
                                          state=DISABLED)
        self.__dice3button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice3_back,
                                          state=DISABLED)
        self.__dice4button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice4_back,
                                          state=DISABLED)
        self.__dice5button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice5_back,
                                          state=DISABLED)
        self.__dice6button_under = Button(self.__main_window,
                                          image=self.__empty_image,
                                          command=self.move_dice6_back,
                                          state=DISABLED)

        self.__dice1button_under.grid(row=7, column=2, rowspan=2, columnspan=2,
                                      padx=20, pady=10)
        self.__dice2button_under.grid(row=7, column=4, rowspan=2, columnspan=2,
                                      padx=20, pady=10)
        self.__dice3button_under.grid(row=7, column=6, rowspan=2, columnspan=2,
                                      padx=20, pady=10)
        self.__dice4button_under.grid(row=9, column=2, rowspan=2, columnspan=2,
                                      padx=20, pady=10)
        self.__dice5button_under.grid(row=9, column=4, rowspan=2, columnspan=2,
                                      padx=20, pady=10)
        self.__dice6button_under.grid(row=9, column=6, rowspan=2, columnspan=2,
                                      padx=20, pady=10)

        """Labels on the right of the screen"""
        self.__player1_points_label = Label(self.__main_window,
                                            text="Player 1 points: ")
        self.__player2_points_label = Label(self.__main_window,
                                            text="Player 2 points: ")
        self.__points_this_turn_label = Label(self.__main_window,
                                              text="Points for this turn: ")
        self.__goal_label = Label(self.__main_window,
                                  text="First to 5000 points wins!")
        self.__goal_label.grid(row=3, column=8, columnspan=3)

        self.__player1_points_label.grid(row=1, column=8, columnspan=3,
                                         sticky=E+W)
        self.__player2_points_label.grid(row=2, column=8, columnspan=3,
                                         sticky=E+W)
        self.__points_this_turn_label.grid(row=5, column=2, columnspan=3)


        self.__player1_points_number = Label(self.__main_window, text=0)
        self.__player2_points_number = Label(self.__main_window, text=0)
        self.__points_this_turn_number = Label(self.__main_window)


        self.__player1_points_number.grid(row=1, column=11, columnspan=2)
        self.__player2_points_number.grid(row=2, column=11, columnspan=2)
        self.__points_this_turn_number.grid(row=5, column=5)

        self.new_game()

    def start(self):
        """ Starts the mainloop. """

        self.__main_window.mainloop()

    def hand_over(self):
        """ Function connected to the 'Score and Pass' Button """

        if self.__WHOSE_TURN % 2 == 0:
            self.__player1_points += self.__round_points
            self.__player1_points_number.configure(text=self.__player1_points)

            self.change_turn()
        else:
            self.__player2_points += self.__round_points
            self.__player2_points_number.configure(text=self.__player2_points)
            self.change_turn()

    def change_turn(self):
        """This is called during bust or during handover (Score and pass)"""

        # Determines if the game has been won this round
        if self.is_over():
            return

        self.__thrownumber = 0
        self.__WHOSE_TURN = (self.__WHOSE_TURN + 1 ) % 2
        self.__instructions = "Player " + str(self.__WHOSE_TURN + 1) + \
                              "'s turn to throw the dices"
        DICES_SET_ASIDE_THIS_ROUND.clear()
        DICES_THROWN.clear()
        self.reset_view()

        self.update_scores()

    def game_over_mode(self):
        """To be activated when either of the players have won"""
        self.reset_view()
        self.__throw_button.configure(state=DISABLED)
        self.__score_and_roll_again.configure(state=DISABLED)

    def is_over(self):
        """ Determines if either of the player has reached the required 5000
        points for the victory

        :return: Boolean value, True, if someone has won
        False, if no one has won
        """
        if int(self.__player1_points_number["text"]) >= 5000:
            self.__instructions = "Player 1 has won! Press 'New game/Quit"
            self.update_scores()
            self.game_over_mode()
            return True
        elif int(self.__player2_points_number["text"]) >= 5000:
            self.__instructions = "Player 2 has won! Press 'New game/Quit"
            self.update_scores()
            self.game_over_mode()
            return True
        else:
            return False

    def reset_view(self):
        """Resets certain buttons and images to a default"""
        self.__dice1button.configure(image=self.__dice_images[0], state=DISABLED)
        self.__dice2button.configure(image=self.__dice_images[1], state=DISABLED)
        self.__dice3button.configure(image=self.__dice_images[2], state=DISABLED)
        self.__dice4button.configure(image=self.__dice_images[3], state=DISABLED)
        self.__dice5button.configure(image=self.__dice_images[4], state=DISABLED)
        self.__dice6button.configure(image=self.__dice_images[5], state=DISABLED)
        self.__throw_button.configure(state=NORMAL)
        self.__score_and_pass_button.configure(state=DISABLED)
        self.__dice1button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice2button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice3button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice4button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice5button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice6button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__round_points = 0

    def new_game(self):
        self.__player1_points = 0
        self.__player2_points = 0
        self.__round_points = 0
        self.__WHOSE_TURN = 0

        # 0 means nothing has been thrown yet this round, 1 means it's the
        # first throw of the round, 2 means score and roll again
        # has been pressed.
        self.__thrownumber = 0

        self.__instructions = "Player " + str(self.__WHOSE_TURN + 1) + \
                              "'s turn to throw the dices"
        DICES_SET_ASIDE_THIS_ROUND.clear()
        DICES_THROWN.clear()

        self.reset_view()
        self.update_scores()

    def update_scores(self):
        """Updates points and instructions"""

        self.__player1_points_number.configure(text=self.__player1_points)
        self.__player2_points_number.configure(text=self.__player2_points)
        self.__points_this_turn_number.configure(text=self.__round_points)
        self.__instructions_label.configure(text=self.__instructions)

    def throw(self):
        """Makes the first throw"""

        self.__throw_button.configure(state=DISABLED)
        self.__score_and_pass_button.configure(state=NORMAL)
        self.__thrownumber = 1
        for _ in range(10):
            dice1 = random.randint(1, 6)
            self.__dice1button.configure(image=self.__dice_images[dice1-1], state=NORMAL)
            dice2 = random.randint(1,6)
            self.__dice2button.configure(image=self.__dice_images[dice2 - 1], state=NORMAL)
            dice3 = random.randint(1,6)
            self.__dice3button.configure(image=self.__dice_images[dice3 - 1], state=NORMAL)
            dice4 = random.randint(1,6)
            self.__dice4button.configure(image=self.__dice_images[dice4 - 1], state=NORMAL)
            dice5 = random.randint(1,6)
            self.__dice5button.configure(image=self.__dice_images[dice5 - 1], state=NORMAL)
            dice6 = random.randint(1,6)
            self.__dice6button.configure(image=self.__dice_images[dice6 - 1], state=NORMAL)

            self.__main_window.update_idletasks()
            time.sleep(0.1)

        """Saves information on what the current thrown dices are"""
        DICES_THROWN.append(int(self.__dice1button["image"][-1]))
        DICES_THROWN.append(int(self.__dice2button["image"][-1]))
        DICES_THROWN.append(int(self.__dice3button["image"][-1]))
        DICES_THROWN.append(int(self.__dice4button["image"][-1]))
        DICES_THROWN.append(int(self.__dice5button["image"][-1]))
        DICES_THROWN.append(int(self.__dice6button["image"][-1]))
        if self.is_bust() is False:
            self.change_turn()

    def check_of_kinds(self):
        """Checks if there are any 3, 4, 5 or 6 of kinds thrown, 
        returns True if is"""

        for number in range(6, 0, -1):
            for amount in range(6, 2, -1):
                if DICES_THROWN.count(number) == amount:
                    return True

    def check_additional_of_kinds(self):
        """ Checks for 2 things:
        3 of a kind set aside and 3 of a kind available for choosing
        3 of a kind set aside and a different 3 of a kind set a side too

        """
        for number in range(1,7):
            for number2 in range(1,7):
                if DICES_THROWN.count(
                        number) == 3 and DICES_SET_ASIDE_THIS_ROUND.count(
                        number2) == 3:

                    return True
                elif DICES_SET_ASIDE_THIS_ROUND.count(
                        number) == 3 and DICES_SET_ASIDE_THIS_ROUND.count(
                        number2) == 3 and len(DICES_SET_ASIDE_THIS_ROUND) == 6 and number != number2:
                    return True

        return False


    def check_for_bigger_kinds(self):
        """ If there is a x of a kind set aside, checks if there is
        x+1, x+2 and x+3 of a kind available"""
        for number in range(1,7):
            if DICES_SET_ASIDE_THIS_ROUND.count(number) >= 3 and \
                    DICES_THROWN.count(number) >= 1:
                return True

    def is_bust(self):
        """ Determines if a new roll is a bust (no new points attainable)


        :return: True, if points attainable, false if not attainable
        """

        "If there are new 1's or 5's they can be added for points"

        if 1 in DICES_THROWN or 5 in DICES_THROWN:
            return True
        elif self.check_of_kinds():
            return True
        # checks for straights
        elif [1,2,3,4,5] in DICES_THROWN or [2,3,4,5,6] in DICES_THROWN or \
                [1,2,3,4,5,6] in DICES_THROWN:
            return True
        elif self.check_additional_of_kinds():
            return True
        elif self.check_for_bigger_kinds():
            return True
        else:
            time.sleep(0.5)
            self.__main_window.update()
            self.__instructions = "Bust!"
            self.update_scores()
            self.__main_window.update()
            time.sleep(4)
            return False


    def score_and_roll_again(self):
        """Determines whether a dice has been set aside and
        if not, rolls a new figure for each of them"""

        DICES_THROWN.clear()
        self.__throw_button.configure(state=DISABLED)
        self.__score_and_pass_button.configure(state=NORMAL)
        self.__score_and_roll_again.configure(state=DISABLED)
        self.__thrownumber = 2

        if self.__dice1button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice1button.configure(image=self.__dice_images[dice1-1],
                                             state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice1button_under.configure(state=DISABLED)

        if self.__dice2button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice2button.configure(
                    image=self.__dice_images[dice1 - 1], state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice2button_under.configure(state=DISABLED)

        if self.__dice3button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice3button.configure(
                    image=self.__dice_images[dice1 - 1], state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice3button_under.configure(state=DISABLED)

        if self.__dice4button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice4button.configure(
                    image=self.__dice_images[dice1 - 1], state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice4button_under.configure(state=DISABLED)

        if self.__dice5button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice5button.configure(
                    image=self.__dice_images[dice1 - 1], state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice5button_under.configure(state=DISABLED)

        if self.__dice6button["state"] == "normal":
            for _ in range(10):
                dice1 = random.randint(1, 6)
                self.__dice6button.configure(
                    image=self.__dice_images[dice1 - 1], state=NORMAL)

                self.__main_window.update_idletasks()
                time.sleep(0.02)
        else:
            self.__dice6button_under.configure(state=DISABLED)

        "Determines the new thrown figures and saves them in a list, "
        "removes all the ones with empty images"
        DICES_THROWN.append(int(self.__dice1button["image"][-1]))
        DICES_THROWN.append(int(self.__dice2button["image"][-1]))
        DICES_THROWN.append(int(self.__dice3button["image"][-1]))
        DICES_THROWN.append(int(self.__dice4button["image"][-1]))
        DICES_THROWN.append(int(self.__dice5button["image"][-1]))
        DICES_THROWN.append(int(self.__dice6button["image"][-1]))
        for number in DICES_THROWN:
            if number == 7:
                DICES_THROWN.remove(7)
                continue

        #checks if the new throw is a bust
        if self.is_bust() is False:
            self.change_turn()

    def update_point_label_this_turn(self, points):
        self.__points_this_turn_number.configure(text=points)

    def update_state_of_score_and_roll_again_button(self, points):
        """ Updates the state of the score and roll again button.
        Disabled, if it has already been pressed once this round or
        no points able to be scored.
        Enabled, if it hasn't yet been pressed this round and
        there are points able to be scored.

        :param points: Int, the amount of points from this round
        """
        if self.__thrownumber == 2:
            self.__score_and_roll_again.configure(state=DISABLED)
        elif points > 0:
            self.__score_and_roll_again.configure(state=NORMAL)
        else:
            self.__score_and_roll_again.configure(state=DISABLED)

    """The next methods are for moving the dices up and down physically on the 
    screen when clicked on them. This is the 'selection' of a dice for scoring 
    and the functionalities that come with it like keeping track of which have 
    been selected, which buttons need to be disabled, calculating 
    possible score etc
    
    Only the functions for the first dice is commented, the rest are similar.
    Dices are numbered on the screen as follows: [1 2 3]
                                                 [4 5 6] 
                                                 DIVIDER
                                                 [1 2 3]
                                                 [4 5 6] 
    """
    def move_dice1(self):
        """ Moves dice 1 (upper left corner) from upper area to
         lower 'selected' area.

        """
        #determines the score on the dice based on the image and
        # keeps data on which is up and which is selected down
        dice_score = int(self.__dice1button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)

        #Adds the picture to the bottom and removes it from the top
        self.__dice1button.configure(image=self.__empty_image, state=DISABLED)
        self.__dice1button_under.configure(
            image=self.__dice_images[dice_score-1], state=NORMAL)

        #Calculates the score based on the selected dices
        # and displays it on the screen.
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)

        #If the score and roll again has not yet been pressed this button and
        # there are more than 0 points, activates this button
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice1_back(self):
        """ Moves dice 1 (upper left corner) from lower 'selected' area back
        to upper area.


        """
        # determines the score on the dice based on the image and
        # keeps data on which is up and which is selected down
        dice_score = int(self.__dice1button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)

        # Adds the picture to the top and removes it from the bottom
        self.__dice1button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice1button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)

        # Calculates the score based on the remaining selected dices
        # and displays it on the screen.
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)

        # If the score and roll again has not yet been pressed this button and
        # there are more than 0 points, activates this button
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice2(self):
        dice_score = int(self.__dice2button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)
        self.__dice2button.configure(image=self.__empty_image ,state=DISABLED)
        self.__dice2button_under.configure(
            image=self.__dice_images[dice_score - 1], state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice2_back(self):
        dice_score = int(self.__dice2button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)
        self.__dice2button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice2button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice3(self):
        dice_score = int(self.__dice3button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)
        self.__dice3button.configure(image=self.__empty_image ,state=DISABLED)
        self.__dice3button_under.configure(
            image=self.__dice_images[dice_score - 1], state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)


    def move_dice3_back(self):
        dice_score = int(self.__dice3button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)
        self.__dice3button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice3button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice4(self):
        dice_score = int(self.__dice4button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)
        self.__dice4button.configure(image=self.__empty_image ,state=DISABLED)
        self.__dice4button_under.configure(
            image=self.__dice_images[dice_score - 1], state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice4_back(self):
        dice_score = int(self.__dice4button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)
        self.__dice4button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice4button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice5(self):
        dice_score = int(self.__dice5button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)
        self.__dice5button.configure(image=self.__empty_image ,state=DISABLED)
        self.__dice5button_under.configure(
            image=self.__dice_images[dice_score - 1], state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice5_back(self):
        dice_score = int(self.__dice5button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)
        self.__dice5button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice5button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice6(self):
        dice_score = int(self.__dice6button["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.append(dice_score)
        DICES_THROWN.remove(dice_score)
        self.__dice6button.configure(image=self.__empty_image ,state=DISABLED)
        self.__dice6button_under.configure(
            image=self.__dice_images[dice_score - 1], state=NORMAL)

        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def move_dice6_back(self):
        dice_score = int(self.__dice6button_under["image"][-1])
        DICES_SET_ASIDE_THIS_ROUND.remove(dice_score)
        DICES_THROWN.append(dice_score)
        self.__dice6button_under.configure(image=self.__empty_image,
                                           state=DISABLED)
        self.__dice6button.configure(image=self.__dice_images[dice_score-1],
                                     state=NORMAL)
        self.__round_points = self.calculate_score()
        self.update_point_label_this_turn(self.__round_points)
        self.update_state_of_score_and_roll_again_button(self.__round_points)

    def calculate_score(self):
        """ Calculates the current score based on the dices selected."""

        six_of_kinds = {6: "six of a kind:6", 5: "six of a kind:5",
                        4: "six of a kind:4", 3: "six of a kind:3",
                        2: "six of a kind:2"}
        amount_of_ones = DICES_SET_ASIDE_THIS_ROUND.count(1)
        amount_of_fives = DICES_SET_ASIDE_THIS_ROUND.count(5)

        if DICES_SET_ASIDE_THIS_ROUND.count(1) == 6:
            points = POINTS["six of a kind:1"]
            return points
        else:
            for _ in range(6, 1, -1):
                if DICES_SET_ASIDE_THIS_ROUND.count(_) == 6:
                    points = POINTS[six_of_kinds[_]]
                    return points

        five_of_kinds = {6: "five of a kind:6", 5: "five of a kind:5",
                         4: "five of a kind:4", 3: "five of a kind:3",
                         2: "five of a kind:2"}
        if DICES_SET_ASIDE_THIS_ROUND.count(1) == 5:
            if amount_of_fives > 0:
                points = POINTS["five of a kind:1"] + amount_of_fives * 50
            else:
                points = POINTS["five of a kind:1"]
            return points
        else:
            for _ in range(6, 1, -1):
                if DICES_SET_ASIDE_THIS_ROUND.count(_) == 5:
                    if _ == 5:
                        points = POINTS[five_of_kinds[5]] + amount_of_ones * 100
                    else:
                        points = POINTS[five_of_kinds[_]] + \
                                 amount_of_ones * 100 + \
                                 amount_of_fives * 50
                    return points

        four_of_kinds = {6: "four of a kind:6", 5: "four of a kind:5",
                         4: "four of a kind:4", 3: "four of a kind:3",
                         2: "four of a kind:2"}
        if DICES_SET_ASIDE_THIS_ROUND.count(1) == 4:
            if amount_of_fives > 0:
                points = POINTS["four of a kind:1"] + amount_of_fives * 50
            else:
                points = POINTS["four of a kind:1"]
            return points
        else:
            for _ in range(6, 1, -1):
                if DICES_SET_ASIDE_THIS_ROUND.count(_) == 4:
                    if _ == 5:
                        points = POINTS[four_of_kinds[5]] + amount_of_ones * 100
                    else:
                        points = POINTS[four_of_kinds[_]] + \
                                 amount_of_ones * 100 + \
                                 amount_of_fives * 50
                    return points


        # With three of a kinds, it also calculates if there are 2 different
        # three of a kinds selected, since it's possible.
        three_of_kinds = {6: "three of a kind:6", 5: "three of a kind:5",
                          4: "three of a kind:4", 3: "three of a kind:3",
                          2: "three of a kind:2"}
        if DICES_SET_ASIDE_THIS_ROUND.count(1) == 3:
            if 3 > amount_of_fives > 0:
                points = POINTS["three of a kind:1"] + amount_of_fives * 50
            elif self.check_additional_of_kinds():
                other_number = max(DICES_SET_ASIDE_THIS_ROUND)
                points = POINTS["three of a kind:1"] + POINTS[three_of_kinds[other_number]]
            else:
                points = POINTS["three of a kind:1"]
            return points
        else:
            for dice_front in range(6, 1, -1):
                if DICES_SET_ASIDE_THIS_ROUND.count(dice_front) == 3:
                    if dice_front == 5 and amount_of_ones > 0:
                        points = POINTS[three_of_kinds[5]] + amount_of_ones * 100
                    elif dice_front == 5 and len(DICES_SET_ASIDE_THIS_ROUND) == 3:
                        points = POINTS[three_of_kinds[5]]
                    elif self.check_additional_of_kinds():
                        first_number, second_number = sorted(DICES_SET_ASIDE_THIS_ROUND)[0], sorted(DICES_SET_ASIDE_THIS_ROUND)[-1]
                        points = POINTS[three_of_kinds[first_number]] + POINTS[three_of_kinds[second_number]]
                    else:
                        points = POINTS[three_of_kinds[dice_front]] + \
                                 amount_of_ones * 100 + \
                                 amount_of_fives * 50
                    return points

        "Calculates points of straights, if there are any"
        if 1 in DICES_SET_ASIDE_THIS_ROUND and 2 in DICES_SET_ASIDE_THIS_ROUND \
                and 3 in DICES_SET_ASIDE_THIS_ROUND \
                and 4 in DICES_SET_ASIDE_THIS_ROUND \
                and 5 in DICES_SET_ASIDE_THIS_ROUND\
                and 6 in DICES_SET_ASIDE_THIS_ROUND:
            points = POINTS["full straight"]
            return points
        elif 2 in DICES_SET_ASIDE_THIS_ROUND and 3 in DICES_SET_ASIDE_THIS_ROUND \
                and 4 in DICES_SET_ASIDE_THIS_ROUND \
                and 5 in DICES_SET_ASIDE_THIS_ROUND \
                and 6 in DICES_SET_ASIDE_THIS_ROUND:
            points = POINTS["partial straight 2-6"]
            return points
        elif 1 in DICES_SET_ASIDE_THIS_ROUND and 2 in DICES_SET_ASIDE_THIS_ROUND \
                and 3 in DICES_SET_ASIDE_THIS_ROUND \
                and 4 in DICES_SET_ASIDE_THIS_ROUND \
                and 5 in DICES_SET_ASIDE_THIS_ROUND:
            points = POINTS["partial straight 1-5"]
            return points

        "Calculates points if there's only 1's or 5's set aside"
        if 2 not in DICES_SET_ASIDE_THIS_ROUND \
                and 3 not in DICES_SET_ASIDE_THIS_ROUND \
                and 4 not in DICES_SET_ASIDE_THIS_ROUND \
                and 6 not in DICES_SET_ASIDE_THIS_ROUND:
            points = amount_of_fives * 50 + amount_of_ones * 100
            return points
        else:
            return 0


def main():
    gui = GUI()
    gui.start()


if __name__ == "__main__":
    main()