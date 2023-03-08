from UI import BattleshipUI as BSUI

class Startup(object):
    def __init__(self) -> None:
        self.__db_conn_string = ""
        self.app = BSUI.BattleshipUI()

    def initialize(self):
        self.app.create_login_screen()