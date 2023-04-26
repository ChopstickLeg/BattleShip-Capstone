from UI import BattleshipUI as BSUI
import os

class Startup(object):
    def __init__(self) -> None:
        self.__db_conn_string = ""
        cwd = os.getcwd()
        path = os.path.join(cwd, "Saved_Games")
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
        self.app = BSUI.BattleshipUI()
        

    def initialize(self):
        self.app.__init__()