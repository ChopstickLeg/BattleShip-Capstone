from UI import BattleshipUI as BSUI
import os

class Startup(object):
    def __init__(self) -> None:
        cwd = os.getcwd()
        path = os.path.join(cwd, "Saved_Games")
        try:
            os.mkdir(path)
        except OSError:
            pass
        self.app = BSUI.BattleshipUI()
        

    def initialize(self):
        self.app.__init__()