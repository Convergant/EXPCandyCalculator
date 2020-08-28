from EXPCandy import EXPCandy
import math

class Pokemon:
    def __init__(self, exp_next_level, exp_group):
        """ Construct a Pokémon.

        :param exp_next_level: The EXP required for this Pokémon to level up once.
        :param exp_group: The EXP group this Pokémon is in. """

        self.exp_next_level = exp_next_level
        self.exp_group = exp_group

    """
     Method to determine how many of each kind of candy is needed to reach the target level.
     Takes the initial and final level.
    """
    def candies_needed(self, initial_level, final_level):
        """ Determine how many of each kind of candy is needed to reach the target level.

        :param initial_level: The initial level of the Pokémon.
        :param final_level: The final level of the Pokémon. """
        # Calculate the change in experience required to reach the target level.
        delta_exp = self.__exp_needed(initial_level, final_level)

        # Declare the EXP remaining initially equal to the change in EXP.
        exp_remaining = delta_exp

        candies = [candy for candy in EXPCandy if candy.value.considering]

        # Declare the list of candy amounts initially as many 0s are there are candies.
        candy_amounts = [0]*len([candy for candy in EXPCandy])

        # Loop for every candy.
        for candy in EXPCandy:
            if exp_remaining <= 0:
                break

            # If this candy is being considered, do the calculation for how many of it there should be.
            if candy.value.considering:
                # The number of candies is, ultimately,
                # (total EXP able to be provided by this candy without going over) / (amount of EXP provided by this candy).
                # The numerator is obtained by subtracting the remainder of diving the EXP remaining by the EXP provide
                # from the EXP remaining.

                if candy == candies[-1]:
                    num_candies = int(math.ceil(exp_remaining / candy.candy_amount()))

                else:
                    num_candies = int((exp_remaining - (exp_remaining % candy.candy_amount())) / candy.candy_amount())

                # Subtract the amount of EXP provided by this candy from the EXP remaining.
                exp_remaining -= num_candies*candy.candy_amount()

                # Set this candy's amount to the number of candies used.
                candy_amounts[candy.candy_index()] = num_candies

        # Return the number of each kind of candy used, and the EXP remaining.
        return [candy_amounts, exp_remaining]

    def __exp_needed(self, initial_level, final_level):
        """ Calculate the EXP needed to reach a final level from an initial level.

        :param initial_level: The initial level of the Pokémon.
        :param final_level: The final level of the Pokémon. """

        # EXP needed is the EXP after leveling up - EXP before leveling up.
        # This is calculated by the total EXP at the final level minus the total EXP at the initial level plus 1,
        # plus the level-up EXP.

        return self.exp_next_level + self.exp_group.total_exp(final_level) - self.exp_group.total_exp(initial_level + 1)
