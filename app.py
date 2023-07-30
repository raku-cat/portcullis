from screenutils import list_screens, Screen
import pexpect
import traceback

import MenuBuilder

import os



# Get app's full path to support reading config files when ran from a ForceCommand in sshd_config
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_connections():
    connections = []

    with open(os.path.join(__location__, 'servers.list'), 'r') as servers:
        for line in servers:
            s = line.strip()
            connections.append(s)

    return connections


def QuitApp():
    print("Exiting...")
    exit()


# Probably doesn't need to be in it's own class, too lazy to change it rn..
class ConsoleUtils:

    def clear_screen():
        print("\033[{};1H".format(os.get_terminal_size().lines))
        os.system("clear")



# Handles displaying application Menus using the inclulded MenuBuilder "engine"
class Menu:


    # Iniitiallize layout container and statically assign our title as the app tile
    def __init__(self):
        self.prompt_layout = []
        self.prompt_layout.append(
            { "title" : "Portcullis" }
        )


    # Displays the requested menu, keeps the menu active until until the user enters a valid input
    def show(self, menu_list=None):
        with MenuBuilder.Window(self.prompt_layout) as mb:
            while True:
                if "input" in self.prompt_layout:
                    user_selection = mb.run(capture_input=True)
                    if user_selection is not None:
                        menu_selection = mb.validate_input(user_selection, menu_list)
                        break
            return menu_selection


    # Home menu constructor, returns the user selection
    def home(self):
        main_menu_options = {
            "connect_session": "Connect",
            "list_sessions": "List sessions"
        }

        self.prompt_layout.append(
            { "list" : main_menu_options }
        )

        self.prompt_layout.append("input")
        return self.show(main_menu_options)


    # Connection menu constructor, reeturns the user selection
    def connect(self, connections):
        self.prompt_layout.append(
            { "list" : connections }
        )

        self.prompt_layout.append("input")
        return self.show(connections)


    # Session attach menu constructor, returns the user selection
    def attach(self, sessions):
        self.prompt_layout.append(
            { "list" : sessions }
        )

        self.prompt_layout.append("input")
        return self.show(sessions)


# Main app class, handles displaying menus, menu navigation state, and underlying menu option functions
class Portcullis:

    # Initialize the history list, set our first menu as the home menu, also defines possible menu screens associated with their underlying functions, and navigate to the home menu
    def __init__(self):
        self.navigation_history = []
        self.current_screen = "home"
        self.screens = {
            "home" : self.home,
            "connect_session" : self.connect_session,
            "list_sessions" : self.list_sessions,
        }
        self.navigate(self.current_screen)


    # Displays the currently selected menu, loops to keep the current menu active until navigated away from
    def display(self, selection):
        while True:
            ConsoleUtils.clear_screen()
            self.screens[selection]()


    # Handles naviagation between menus and storing navigation history, currently has static special handling for the back and exit functions
    def navigate(self, selection):
        if selection == "back":
            self.back()
            return
        elif selection == "exit_app":
            QuitApp()
        else:
            self.navigation_history.append(selection)
            self.current_screen = selection
            self.display(self.current_screen)


    # Navigates backwards through menus, stops at home by special handling to just display the current window again if the history contains 1 item which should just be the home menu
    def back(self):
        if len(self.navigation_history) > 1:
            self.navigation_history.pop()
            self.current_screen = self.navigation_history[-1]  # Remove the current menu from history

        self.display(self.current_screen)


    # Displays the home menu and navigates to selected menu
    def home(self):
        menu_selection = Menu().home()
        if menu_selection is not None:
            self.navigate(menu_selection)


    # Handles listing of screen sessions and attaching to a selected screen
    def list_sessions(self):
        sessions = {}
        for session in list_screens():
            sessions.update({session.id : str(session.name + " " + "(" + session.id + ")")})
        menu_selection = Menu().attach(sessions)
        if menu_selection not in list(sessions.keys()):
            self.navigate(menu_selection)
            return
        else:
            selected_session = str(menu_selection)
        try:
            rows = os.get_terminal_size()[0]
            columns = os.get_terminal_size()[1]
            screen_command = f"screen -q -r {selected_session}"
            child = pexpect.spawn(screen_command, dimensions=(rows,columns))
            child.interact()
        except Exception:
            print(traceback.format_exc())


    # Handles listing of configured connections
    def connect_session(self):
        connection_list = get_connections()
        menu_selection = Menu().connect(connection_list)

        if menu_selection not in connection_list:
            self.navigate(menu_selection)
            return
        else:
            selected_connection = str(menu_selection)
        try:
            rows = os.get_terminal_size()[0]
            columns = os.get_terminal_size()[1]
            screen_command = f"screen -q -R {selected_connection} -- ssh {selected_connection}"
            child = pexpect.spawn(screen_command, dimensions=(rows,columns))
            child.interact()
        except pexpect.exceptions.EOF:
            ConsoleUtils.clear_screen()
            print("The screen session has ended.")
        except pexpect.exceptions.TIMEOUT:
            print("Timed out waiting for the screen session.")
            print("screen closed")
        except Exception:
            print(traceback.format_exc())



if __name__ == "__main__":
    while True:
        try:
            Portcullis()
        except KeyboardInterrupt:
            QuitApp()
        except Exception as e:
            print(traceback.format_exc())
