from Card import Card          #import Card class
from tkinter import PhotoImage  #import module to use images
import random                   #import module to use random functions

class DeckOfCards:

    """
    Creates a card deck object to store the card objects.

    VARS:
    -----
    deck: list
        The card deck.
    numberslist: list
        List holding values of the 13 types of cards in a deck.
    suits: list
        List holding the card suits.
    index: int
        Indexing value.
    """

    def __init__(self):
        self.__deck = [0] * 52
        self.__numberslist = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        self.__suits = ("C", "D", "H", "S")
        index = 0

        for n in range(len(self.__numberslist)):    #cycle through each card
            for s in range(len(self.__suits)):
                self.__deck[index] = Card()         #create 52 Card objects
                self.__deck[index].set_image(PhotoImage(file="images/" +
                                                        str(self.__numberslist[n])
                                                        + self.__suits[s] + ".png"))    #set the appropriate card img
                if 10 <= self.__numberslist[n] <= 13:
                    self.__deck[index].set_value(0)
                elif self.__numberslist[n] == 14:       #Change certain card values in relation to Baccarat rules
                    self.__deck[index].set_value(1)
                else:
                    self.__deck[index].set_value(self.__numberslist[n])     #set normal card value to each object

                index += 1

        self.shuffle_deck()     #shuffle the deck list whenever it is created (for dealing cards)

    def deal_card(self, i):

        """
        Deal a card object.

        PARAMETER:
        ----------
        i = int
            Indexing value to deal 6 cards from the deck.

        RETURN:
        -------
        Card
            A Card object.
        """

        return self.__deck[i]

    def shuffle_deck(self):

        """
        Shuffle the deck list.

        RETURN:
        -------
        list
            The deck list.
        """

        return random.shuffle(self.__deck)
