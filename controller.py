__author__ = 'DerekHu'


from api_wrapper import DribleAPI
from models import User
from views import View
from player import MPC


class Controller():

    def __init__(self, user=None):
        self.api = DribleAPI()
        self.view = View()
        self.user = user
        self.player = MPC()
        self.current_station = None

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
                print(current_station['streamurl'])
                player_status = self.player.add('http://37.187.79.56:3042/stream')

                while True:
                    choice = self.view.player_menu(player_status)
                    if choice == '1':
                        self.player.stop()
                        break


            else:
                continue


if __name__ == '__main__':
    c = Controller()
    c.login()