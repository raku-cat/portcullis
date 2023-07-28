from screenutils import list_screens, Screen
import pexpect


import random


class InvalidPromptException(Exception):
    pass

def QuitApp():
    print("Exiting...")
    exit()


class Prompt:
    
    def __init__(self, options):
        if isinstance(options, (list, dict)):
            self.options = options
        else:
            raise InvalidPromptException("Invalid Prompt options, expected type `list` or `dict`, got: "  + type(options).__name__)

    def show(self):
        #print(chr(27) + "[2J")
        if isinstance(self.options, dict):
            self.options_values = list(self.options.values())
        else:
            self.options_values = self.options
        for number, option in enumerate(self.options_values, 1):
            print(str(number) + ".", option)
        print("e = exit, b = back")

    def input(self):
        print("-"*30)
        self.user_selection = input("Select menu option: ")

    def invalid_input(self):
        input("lnvalid option, press any key to continue...")
        return None
   
    def validate_input(self): 
        if isinstance(self.options, dict):
            self.option_keys = list(self.options.keys())
        elif isinstance(self.options, list):
            self.option_keys = self.options
        try:
            self.user_selection = int(self.user_selection)
            if 1 <= self.user_selection <= len(self.options):
                self.user_selection = self.option_keys[self.user_selection - 1]
                self.validated_selection = self.user_selection
            else:
                self.invalid_input()
        except ValueError:
            if isinstance(self.user_selection, str):
                if self.user_selection == "e":
                    self.validated_selection = "exit_app"
                elif self.user_selection == "b":
                    self.validated_selection = "back"
                else:
                    self.invalid_input()
            else:
                self.invalid_input()
        except Exception as e:
            print(e)


    def run(self):
        self.validated_selection = None

        while self.validated_selection is None:  # Keep the loop running until a valid input is received or KeyboardInterrupt occurs.
            try:
                self.show()
                self.input()
                self.validate_input()
                if self.validated_selection is not None:
        #            print("picked: " + self.validated_selection)
                    return self.validated_selection
                    break  # Break the loop if a valid input is received.

#            except KeyboardInterrupt:
#                exit()  # Break the loop if KeyboardInterrupt occurs.

            except Exception as e:
                print(e)




class Menu:
    
    def main(self):
        main_menu_options = {
            "connect": "Connect",
            "list": "List sessions"
        }

        main_menu = Prompt(main_menu_options)
        main_selection = main_menu.run()
        return main_selection


    def connect(connections):
        if connections is not None:
            connect_menu = Prompt(connections)
        selected_connection = connect_menu.run()
        return selected_connection
    

class Portcullis:
    
    def __init__(self):
        self.menu_history = []  # Store the history of displayed menus
        self.navigate()


    def navigate(self):
        while True:
            main_selection = Menu().main()
            self.menu_history.append(main_selection)
        #    print("main selection was: " + main_selection)
            getattr(self, main_selection)()


    def back(self):
        if len(self.menu_history) > 1:
            self.menu_history.pop()  # Remove the current menu from history
            previous_menu = self.menu_history.pop()  # Get the previous menu
            getattr(self, previous_menu)()  # Display the previous menu

    def exit_app(self):
        QuitApp()
    
    def get_connections(self):
        connections = []
        with open(r'./servers.list', 'r') as servers:
            for line in servers:
                s = line.strip()
                connections.append(s)
        return connections



    def connect(self):
        conn_list = self.get_connections()
        while True:
            selected_connection = Menu.connect(conn_list)
            if selected_connection == "exit_app":
                self.exit_app()
            elif selected_connection == "back":
                self.back()
                return
            else:
                try:
                    screen_command = str("screen -R " + selected_connection + " -- " + "ssh " + selected_connection)

                    child = pexpect.spawn(screen_command)
                    child.interact()  # This will connect your script to the screen session
                except pexpect.exceptions.EOF:
                    print("The screen session has ended.")
                except pexpect.exceptions.TIMEOUT:
                    print("Timed out waiting for the screen session.")    
            
        


if __name__ == "__main__":
    while True:
        try:
            Portcullis()
        except KeyboardInterrupt:
            QuitApp()
        except Exception as e:
            print("Error:", e)
