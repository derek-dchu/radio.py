__author__ = 'DerekHu'


from api_wrapper import DribleAPI
from models import User
from views import View
from mpd import MPDClient, ConnectionError, CommandError


class Controller():

    def __init__(self, user=None):
        self.api = DribleAPI()
        self.view = View()
        self.user = user
        self.player = MPDClient()
        self.current_station = None

        ## Setup MPDClient
        self.player.timeout = 10
        self.player.idletimeout = None
        self.player.connect("localhost", 6600)

    def login(self):
        while True:
            username = self.view.login()

            if username == "exit()":
                break

            self.user = User.get(username=username)

            ## User not found
            if self.user is None:
                ans = self.view.user_not_found(username)
                if ans == 'y' or ans == 'Y':
                    if User.create(username=username) is None:
                        self.view.error()
                    continue
            else:
                self.__user_menu()


    def __user_menu(self):
        while True:
            choice = self.view.user_menu(self.user.username)

            ## Logout
            if choice == '5':
                break

            elif choice == '1':
                current_station = self.api.get_random_station()
                self.player.add(current_station['streamurl'])
                self.player.play()

                while True:
                    choice = self.view.player_menu(current_station['name'], self.player.status()['volume'])
                    if choice == '1':
                        ## Make sure connection
                        try:
                            self.player.connect("localhost", 6600)
                        except ConnectionError:
                            ## already connected
                            pass

                        self.player.stop()
                        self.player.clear()
                        break

                    elif choice == '2':
                        vol = self.view.user_prompt('Set volume to (0~100): ')
                        try:
                            self.player.setvol(vol)
                        except CommandError:
                            self.view.error("Invalid volume value, only accept an integer between 0-100")

            else:
                continue

if __name__ == '__main__':
    c = Controller()
    c.login()