import os
import traceback


# Usage:
#     my_menu_list = [
#         "Orange",
#          "Apple",
#          "Pear"
#     ]
#
#     layout = [
#         {"title" : "My Menu"},
#         {"list" : my_menu_list }, # This can be supplied with a literal python list or a dict
#         "input"} # Will prompt for input, prompt text is static to ask for a menu option
#     my_menu = MenuBuilder.Window(layout)
#     user_response = my_menu.run(capture_input=True) # Can be set to False to ignore input and simply return on input
#     validated_response = my.menu(validate(input, user_response, my_menu_list)
#     print(validated_response)
#     >>> "Apples"
#
# Other functions:
#     [ "separator" ] # Separator() Will print a seprator line of `=` the width of the terminal
# Currently is statically configured to display an additional menu line for the Back and Exit option keys
# Separators are automatically inserted where i consider appropriate

class Window:

    def __init__(self, layout):
        if isinstance(layout, (list)):
            self.layout = layout
        else:
            raise self.InvalidLayoutException("Invalid layout object, expected type `list`, got: "  + type(options).__name__)
        self.width = os.get_terminal_size()[0]
        self.output = None


    def __enter__(self):
        return self


    def InvalidLayoutException(Exception):
        pass


    # Takes a single argument of the text for the title, prints it inline with a separator for prettiness
    def title(self, titletext):
        self.separator(ending="\r")
        print(titletext + " ")


    # Takes two optional arguments to modify the length of the separator, which defaults to the terminal width otherwise, and the line ending for the print command
    def separator(self, length=None, ending="\n"):
        if length is None:
            length = self.width
        print("="*length, end=ending)


    # Takes a single argument of a list or dict of your menu options
    # If a list, list items are printed as list options. If a dict, uses the value of the keys as the list options
    def list(self, options):
        if isinstance(options, dict):
            options_values = list(options.values())
        else:
            options_values = options
        for number, option in enumerate(options_values, 1):
            print(str(number) + ".", option)
        # Always include an exit and back option prompt, static for now
        print("| b = Back | e = Exit |")

        self.separator()


    # Prompts for input and returns the raw input, helper validator function is included
    def input(self):
        user_input = input("Select menu option: ")
        return user_input

    # We return None on invalid input, let the upstream code deal with what happens in that case
    def invalid_input(self):
        input("lnvalid option, press any key to continue...")
        return None


    # Takes the user's input retrieved from the input() command (though could technically be artificially supplied an input..) and the original option list as arguments
    # Parses the input against the original option list and validates the input is a valid selection
    # Returns None and prints an "Invalid option" text if input was invalid in any way, returns the associated key from a dict for `dict` option lists and the list items for `list` option lists
    def validate_input(self, user_input, options):
        validated_input = None
        # The menu options list could be a dict or a list
        if isinstance(options, dict):
            option_keys = list(options.keys())
        elif isinstance(options, list):
            option_keys = options

        # Input could be a list number or letter option
        try:
            user_input = int(user_input)
            if 1 <= user_input <= len(options):
                validated_input = option_keys[user_input - 1]
            else:
                self.invalid_input()
        # Handle lettters, staticly defined to handle exit and back only for now
        except ValueError:
            if isinstance(user_input, str):
                if user_input == "e":
                    validated_input = "exit_app"
                elif user_input == "b":
                    validated_input = "back"
                else:
                    self.invalid_input()
            else:
                self.invalid_input()
        except Exception as e:
            print(e)
            return
        try:
            if validated_input:
                return validated_input
        except Exception as e:
            print("broken: " + str(e))
            print(traceback.format_exc())

    # Main menu window display function, parses each line of the layout and executes the function associated with each element's display
    # Takes a single optional `capture_input` argument of True or False but defaults to False.
    # `capture_input` enables or disables returning the input when an input element is included in the layout, otherwise nothing is returned
    def run(self, capture_input=False):
        for element in self.layout:
            if isinstance(element, str):
                if capture_input:
                    if element == "input":
                        return self.input()
                else:
                    getattr(self, element)()
            elif isinstance(element, dict):
                for subelement, options in element.items():
                    getattr(self, subelement)(options)


    def __exit__(self, exc_type, exc_value, traceback):
        pass

