from imports import Enum


class Candy:
    """ Class for a candy as stored by the EXPCandy object; stores whether it is being considered or not.
     Yes, this is necessary. I would just set each value in EXPCandy to True then change it appropriately,
     but the module for enums I'm using doesn't let you do that, so instead I have to store it in a separate class. """

    def __init__(self, considering):
        """ Construct a candy.

        :param considering: Whether this candy is being considered or not."""
        self.considering = considering

    def update(self):
        """ Flip whether this candy is being considered or not. """
        self.considering = not self.considering


class EXPCandy(Enum):
    """ Enum for the kinds of candy.

    Stores the kinds of candy and whether this candy is being considered. """

    # Initialise all of the candies as being considered.
    XL = Candy(True)
    L = Candy(True)
    M = Candy(True)
    S = Candy(True)
    XS = Candy(True)

    def candy_index(self):
        """ Get the index of this candy. """
        indices = {
            "XL": 0,
            "L": 1,
            "M": 2,
            "S": 3,
            "XS": 4,
        }

        return indices.get(self.name)

    def candy_amount(self):
        """ Get the amount of EXP yielded by an EXP candy.

        30,000 for XL, 10,000 for L, 3,000 for M, 800 for S, 100 for XS. """
        amounts = {
            "XL": 30000,
            "L": 10000,
            "M": 3000,
            "S": 800,
            "XS": 100,
        }

        return amounts.get(self.name)
