__author__ = 'DerekHu'


from blessings import Terminal # for formatting TUI

t = Terminal()

class View:
    def __init__(self):
        pass

    ## clear page
    def clear(self):
        return
        print(t.clear)

    def user_prompt(self, string):
        return input(string)

    def error(self, string=""):
        print("Error: {}".format(string))
        input("Press enter to continue")

    def login(self):
        self.clear()
        return input('''
    Welcome !

    user name: ''')

    def user_menu(self, username):
        self.clear()
        return input('''
    Welcome to {}!

    [1] Just Listen
    [2] Search Station
    [3] Favourite Stations
    [4] Favourite Categories
    [5] Log Out

    Your choice: '''.format(username))

    def user_not_found(self, username):
        self.clear()
        return input('''
    User name not found. Would you like to create an new account with username: {}? (Y/N)
    '''.format(username))

    def player_menu(self, player_status):
        self.clear()
        return input('''
    {}

    [1] Stop
    [2] Volume control

    Your choice: '''.format(player_status))