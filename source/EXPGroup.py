from imports import Enum
import math

class EXPGroup(Enum):
    """ Enum for the EXP groups.

     Stores the kinds of EXP groups, and has a method to calculate the total EXP at a level. """

    # Initialise all of the possible EXP groups.
    ERRATIC = 1
    FAST = 2
    MEDIUM_FAST = 3
    MEDIUM_SLOW = 4
    SLOW = 5
    FLUCTUATING = 6

    def total_exp(self, level):
        """ Get the total EXP.
        :param level: The current level of the Pokémon in this EXP group. """

        # Set the EXP to the value for this EXP group at this level.
        if level == 1:
            return 0

        if self.name == "ERRATIC":
            EXP = self.__erratic_total_exp(level)

        elif self.name == "FAST":
            EXP = self.__fast_total_exp(level)

        elif self.name == "MEDIUM_FAST":
            EXP = self.__mediumfast_exp_at_level(level)

        elif self.name == "MEDIUM_SLOW":
            EXP = self.__mediumslow_total_exp(level)

        elif self.name == "SLOW":
            EXP = self.slow_total_exp(level)

        elif self.name == "FLUCTUATING":
            EXP = self.__fluctuating_total_exp(level)

        return EXP

    @staticmethod
    def __erratic_total_exp(level):
        """ Get the total EXP of a Pokémon in the Erratic EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        if level < 50:
            EXP = int(level ** 3 * (100 - level) / 50)

        elif level < 68:
            EXP = int(level ** 3 * (150 - level) / 50)

        elif level < 98:
            EXP = int(level ** 3 * math.floor((1911 - 10 * level) / 3) / 500)

        else:
            EXP = int(level ** 3 * (160 - level) / 50)

        return EXP

    @staticmethod
    def __fast_total_exp(level):
        """ Get the total EXP of a Pokémon in Fast EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        return int((level ** 3) * 4 / 5)

    @staticmethod
    def __mediumfast_exp_at_level(level):
        """ Get the total EXP of a Pokémon in the Medium Fast EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        return int(level ** 3)

    @staticmethod
    def __mediumslow_total_exp(level):
        """ Get the total EXP of a Pokémon in the Medium Slow EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        return int((level ** 3) * 6 / 5 - 15 * (level ** 2) + 100 * level - 140)

    @staticmethod
    def slow_total_exp(level):
        """ Get the total EXP of a Pokémon in the Slow EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        return int((level ** 3) * 5 / 4)

    @staticmethod
    def __fluctuating_total_exp(level):
        """ Get the total EXP of a Pokémon in the Fluctuating EXP group.

        :param level: The current level of the Pokémon in this EXP group. """
        if level < 15:
            EXP = int(level ** 3 * math.floor((level + 1) / 3 + 24) / 50)

        elif level < 36:
            EXP = int(level ** 3 * (level + 14) / 50)

        else:
            EXP = int(level ** 3 * (math.floor(level / 2) + 32) / 50)

        return EXP

    def __str__(self):
        return "".join([c[0] + c[1:].lower() + " " for c in self.name.split("_")])

