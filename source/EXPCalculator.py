# This is a program which calculates what number of each EXP candy in Pokémon Sword and Shield would be required
# to level up a given Pokémon to a specific level.

# Get all of the necessary imports.
from imports import *
from tkinter import *


# This is the class for a particular UI element; a box to display how much of an EXP candy is needed.
# It also has a button which toggles whether the calculation considers those candies,
# so if you don't have enough of that kind of candy. you can exclude it, and a label for the kind of candy.
class EXPCandyBox:
    """ Class which displays a box for the quantity of a kind of candy.

    Includes a button to toggle whether this candy is being considered, and a label describing the candy. """
    def __init__(self, button_row, button_column, candy, button_width=5, button_height=1, field_width=25, field_bg="gray45", field_fg="white",
                 label_text="", label_bg="gray35", label_fg="white", button_texts=["ON", "OFF"], button_colours=["blue", "red"]):
        """ Construct a candy box at a position for a candy.

        :param button_row: The row the button inhabits.
        :param button_column: The column the button inhabits.
        :param candy: The candy this box represents.
        :param button_width: The width of the toggle button.
        :param button_height: THe height of the toggle button.
        :param field_width: The width of the display field.
        :param field_bg: The background colour of the display field.
        :param field_fg: The foreground colour of the display field.
        :param label_text: The text displayed by the label.
        :param label_bg: The background colour of the label.
        :param label_fg: The foreground colour of the label.
        :param button_texts: The possible text values the button can have.
        :param button_colours: The possible text colours the button can have. """

        self.__candy = candy

        # The toggle button is a Button widget, as provided by tkinter, at the location specified
        # with default text "ON", default text colour blue, a width of 5, height of 1,
        # and an on-click command which toggles its colour and text.
        self.__toggle_button = Button(root, text="ON", command=self.__update_button, fg="blue", width=button_width, height=button_height)
        self.__toggle_button.grid(row=button_row, column=button_column)

        # The text field is 1 column ahead of the button.
        self.__text_field = Label(root, width=25, bg=field_bg, fg=field_fg)
        self.__text_field.grid(row=button_row, column=button_column + 1, columnspan=1, rowspan=1)

        # The text label is 2 columns ahead of the button.
        self.__text_label = Label(root, text=label_text, bg=label_bg, fg=label_fg)
        self.__text_label.grid(row=button_row, column=button_column + 2)

        self.__button_texts = button_texts
        self.__button_colours = button_colours

    def set_text_field(self, value):
        """ Set the value of the text field to a given value. """
        self.__text_field.config(text=str(value))

    def reset(self):
        """ Clear the contents of the text field, and reset the button state. """
        self.__text_field["text"] = ""
        self.__toggle_button["text"] = self.__button_texts[0]
        self.__toggle_button["fg"] = self.__button_colours[0]

    def __update_button(self):
        """ Toggle the text displayed by the button and its colour, and update that EXP candy to toggle whether its
        considered. """

        index = (self.__button_texts.index(self.__toggle_button["text"]) + 1) % len(self.__button_texts)

        self.__toggle_button["text"] = self.__button_texts[index]
        self.__toggle_button["fg"] = self.__button_colours[index]
        EXPCandy[self.__candy.name].value.update()


class IntegerInputBox:
    """ Class for an input box that only accepts integers, using the tkinter library.

    Allows for a minimum, maximum and default value. You can also specify the position, label text, width, column span
    and the error label used."""
    def __init__(self, row, column, label_text="", min=-math.inf, max=math.inf, default=None, input_width=25, column_span=1, error_label=None,
                 input_bg="gray45", input_fg="white", label_bg="gray35", label_fg="white"):
        """  Construct an integer input box at the position specified.

        :param row: The row that the input field will inhabit.
        :param column: The column that the input field will inhabit.
        :param label_text: The text of the label
        :param min: The minimum value the field will accept.
        :param max: The maximum value the field wiill accept.
        :param default: The default value of the field. The field will not display this value.
        :param input_width: The width of the input field.
        :param column_span: The column-span of the input field.
        :param error_label: The error label this object will use to display errors.
        :param input_bg: The background colour of the input field.
        :param input_fg: The foreground colour of the input field.
        :param label_bg: The background colour of the label.
        :param label_fg: The foreground colour of the label. """

        # Assert that the upper bound is greater than the lower bound, and display an error message if not.
        try:
            assert max > min

        except AssertionError:
            msg = "The upper bound must be greater than the lower bound."

            if error_label:
                error_label.config(text=msg)

            else:
                print(msg)

        # The input field is an Entry box (as provided by tkinter), located at the position specified.
        self.__input_field = Entry(root, width=input_width, bg=input_bg, fg=input_fg)
        self.__input_field.grid(row=row, column=column, columnspan=column_span)

        # The label is 1 column ahead of the input box.
        self.__label = Label(root, text=label_text, bg=label_bg, fg=label_fg)
        self.__label.grid(row=row, column=column + 1)

        # Set the min, max and default values.
        self.__min = min
        self.__max = max
        self.__default = default

        # Set the error label.
        self.__error_label = error_label

    def get(self):
        """ Return the value contained in the input field, if it is valid. """
        value = self.__input_field.get()

        # Call the validation check method, and if it passes, return the value.
        if self.__validate(value):
            return self.__validate(value)

    def set(self, value):
        """ Set the stored value of the input field, if the given value is valid. """
        if self.__validate(value):
            self.clear()
            self.__input_field.insert(0, str(value))

    def clear(self):
        """ Clear the input field. """
        self.__input_field.delete(0, "end")

    def __validate(self, value):
        """ Validate the value contained in this field. """
        try:
            # Assert that the value or the default exists, assert that the value is an integer,
            # assert that if there is a min value, that it is greater than or equal to it,
            # and that if there is a max value, that it is less than or equal to it.
            assert value or self.__default

            if not value and self.__default:
                value = self.__default

            elif value:
                value = int(value)

            assert int(value) == float(value)

            if self.__min:
                assert self.__min <= value

            if self.__max:
                assert self.__max >= value

        # Catch any assertion errors generated, AKA it didn't pass the validation check.
        except AssertionError:
            # Declare the message initially. Only one error will be shown at a time.
            msg = "Value of " + self.__label["text"] + "\n must be "

            # If the value is empty (i.e. none was inputted and there is no default),
            # make the message that the value must be given.
            if not value:
                msg += "given."

            # If the value is not an integer, make the message that it must be an integer.
            elif int(value) != float(value):
                msg += "an integer."

            # If the value is not less than or equal to the max or greater than or equal to the min,
            # make the message that it must be between the two.
            elif self.__min and self.__max:
                msg += "between\n" + str(self.__min) + " and " + str(self.__max) + "."

            # If only the min exists, then say that the value must be greater than or equal to the min.
            elif self.__min:
                msg += "greater than or equal to " + str(self.__min) + "."

            # If only the max exists, then say that the value must be less than or equal to the min.
            else:
                msg += "less than or equal to " + str(self.__max) + "."

            # Display an error message.
            if self.__error_label:
                self.__error_label.config(text=msg)

            else:
                print(msg)

            # Return False, since the validation test was failed.
            return False

        # Return the value, since it is known to be valid.
        return value


def display_candies(displaying=True):
    """ Display the number of each type of candy.

    :param displaying: Whether the method will actually display, or just return the excess EXP generated.
    :return excess_exp: The excess experience generated by using the candies calculated. """

    # Get the initial and final levels.
    initial_level = init_level_box.get()
    final_level = final_level_box.get()

    # DIsplay and error message if the final level is not greater than the initial level.
    if final_level <= initial_level:
        label_below.config(text="The final level must be\ngreater than the initial level.")
        return

    # Get the EXP to the next level.
    exp_next_level = exp_next_box.get()

    # If the input has passed all the test, clear the error message and display the candies.
    if initial_level and final_level and exp_next_level:
        # Clear the error message.
        label_below.config(text="")

        # Get this Pokémon and the candies needed from it.
        pokemon = Pokemon(exp_next_level, exp_group)
        data = pokemon.candies_needed(initial_level, final_level)
        candies = data[0]
        excess_exp = -data[1]

        if displaying:
            label_below.config(text="Excess EXP: " + str(excess_exp))

            # Loop over every candy.
            for i in range(len(candies)):
                # Set this EXP candy's text box to contain the number of this kind of candy.
                exp_candy_boxes[i].set_text_field(candies[i])

        return excess_exp


def display_ui():
    """ Display the UI for this program.

    The UI broadly consists of the following elements:
        - An auto-completing drop-down entry box, for which Pokémon is being used.
        - An integer input box for the initial level.
        - An integer input box for the final level.
        - An integer input box for the EXP to the next level.
        - An EXPCandyBox for each of the XL, L, M, S, and XS candies.
        - A button to calculate and display the number of each candy needed.
        - A button to level the Pokémon in question up to the target level.
        - A button to reset the inputted information. """

    # The pokemon field should have the first Pokémon, alphabetically, auto-selected.
    clicked = StringVar()
    clicked.set(list(exp_groups_data.keys())[0])

    # Create the pokemon field; its values are the list of keys for exp_groups_data,
    # and its position is row 0 and column 1.
    pokemon = AutocompleteCombobox(root, textvariable=clicked, values=list(exp_groups_data.keys()))
    pokemon.grid(row=0, column=1, columnspan=1)
    pokemon.set_completion_list(list(exp_groups_data.keys()))

    # Get the experience group from the pokemon field.
    global exp_group
    exp_group = exp_groups_data.get(pokemon.get())

    # Declare the inital level box, final level box, EXP to level up box,
    # list of EXP candy boxes, and label below everything else as global variables.
    global init_level_box, final_level_box, exp_next_box, exp_candy_boxes, label_below

    # Create the label below.
    label_below = Label(root, text="", bg="gray35", fg="white")
    label_below.grid(row=len(EXPCandy) + 7, column=1)

    # Create the initial and final level boxes.
    init_level_box = IntegerInputBox(1, 1, label_text="Initial Level", min=1, max=100, default=1, error_label=label_below)
    final_level_box = IntegerInputBox(2, 1, label_text="Final Level", min=1, max=100, default=1, error_label=label_below)

    # Get hte initial level.
    init_level = init_level_box.get()

    # Create the EXP to level up box.
    exp_next_box = IntegerInputBox(3, 1, label_text="EXP To Next Level", min=0,
                                   default=exp_group.total_exp(init_level + 1) - exp_group.total_exp(init_level),
                                   error_label=label_below)

    # Create a list of the input boxes.
    input_boxes = [init_level_box, final_level_box, exp_next_box]

    def update_data():
        """ Update the stored data. Used by the level up button. """

        # Reset every candy box.
        for candy_box in exp_candy_boxes:
            candy_box.reset()

        # Calculate the excess experience, set the initial level to the final level, clear the final level,
        # and calculate the EXP to the next level.
        excess_exp = display_candies(displaying=False)
        init_level_box.set(final_level_box.get())
        final_level_box.clear()
        level = init_level_box.get()
        exp_next_box.set(exp_group.total_exp(level+1) - exp_group.total_exp(level) - excess_exp)

    def reset():
        """ Reset the stored data. Used by the reset button. """

        # Reset every candy box.
        for candy_box in exp_candy_boxes:
            candy_box.reset()

        # Clear every box.
        for box in input_boxes:
            box.clear()

    # Create the calculate button, which when clicked, calls the display_candies() method.
    calculate_button = Button(root, text="Calculate", command=display_candies, width=8)
    calculate_button.grid(row=len(EXPCandy) + 4, column=1)

    # Create the level up button, which when clicked, calls the update_data() method.
    level_up_button = Button(root, text="Level up", command=update_data, width=8)
    level_up_button.grid(row=len(EXPCandy) + 5, column=1)

    # Create the reset button, which when clicked, calls the reset() method.
    reset_button = Button(root, text="Reset", command=reset, width=8)
    reset_button.grid(row=len(EXPCandy) + 6, column=1)

    # Create a label which displays the EXP group of the selected Pokémon.
    exp_group_label = Label(root, text=str(exp_group), bg="gray35", fg="white")
    exp_group_label.grid(row=0, column=2)

    # Declare a list of the boxes for each EXP candy.
    exp_candy_boxes = []

    # Loop over every candy, and create an EXPCandyBox for each candy.
    for candy in EXPCandy:
        exp_candy_boxes.append(EXPCandyBox(candy.candy_index() + 4, 0, candy, label_text="Number of " + candy.name + " candies"))

    # Loop forever:
    while True:
        # Get the EXP group, update the label, and update the root.
        exp_group = exp_groups_data.get(pokemon.get())
        exp_group_label["text"] = str(exp_group)
        root.update()


def main():
    """ Main method of EXPCalculator. """

    # Declare the root of the UI.
    global root
    root = Tk()

    # Get and display the background image.
    photo = PhotoImage(file="background.png")
    label = Label(image=photo)
    label.image = photo  # keep a reference!
    label.place(x=0, y=0, relwidth=1, relheight=1)

    # Set the title of the UI.
    root.title("EXP Calculator")

    root.geometry("800x584")

    # Display the UI.
    display_ui()


if __name__ == '__main__':
    main()

