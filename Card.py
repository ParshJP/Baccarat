from tkinter import PhotoImage  #import module for using images

class Card:

    """
    Creates a card object.

    VARS:
    -----
    value: int
        The card's (number) value
    imgCard: PhotoImage
        The face of the card (back or front).

    PARAMETERS:
    -----------
    color: int
        Value to decide if card has red (banker) or blue (player) back.
    """

    def __init__(self, color = 0):
        self.__value = 0
        if color == 0:
            self.__imgCard = PhotoImage(file="images/back_blue.png")
        else:
            self.__imgCard = PhotoImage(file="images/back_red.png")

    def get_image(self):

        """
        Returns the image of the card.

        RETURNS:
        --------
        PhotoImage
            The image of the card.
        """

        return self.__imgCard

    def get_value(self):

        """
        Returns the value of the card.

        RETURNS:
        --------
        int
            The value of the card.
        """

        return self.__value

    def set_image(self, img):

        """
        Sets the image of the card.

        PARAMETERS:
        -----------
        PhotoImage
            The image of the card.
        """

        self.__imgCard = img

    def set_value(self, cardval):
        """
        Sets the value of the card.

        PARAMETERS:
        -----------
        int
            The value of the card.
        """
        self.__value = cardval
