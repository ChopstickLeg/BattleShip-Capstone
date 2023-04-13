import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from Core.Data import globals

class EndgameScreen(UII):   
    def add_elements(self):
        self.endgame_screen = pygame_menu.Menu("Game Over", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.endgame_screen.add.label("Game Over, " + globals.game_winner[0].user + " won!")
        self.endgame_screen.add.button("Rematch", self.rematch)
        self.endgame_screen.add.button("Return to login")
        self.endgame_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.endgame_screen)
        self.endgame_screen.enable()
        self.run_screen(self.endgame_screen)
    
    def rematch(self):
        globals.game_winner.clear()
        #board = globals.services[1].generate_board(globals.rules[0][0], globals.rules[0][1], globals.rules[0][2], globals.rules[0][3], globals.rules[0][4], globals.rules[0][5], globals.rules[0][6], globals.rules[0][7], globals.rules[0][8])
        globals.rematch.append(True)
    
    def return_to_login(self):
        globals.game_winner.clear()
        globals.account1.clear()
        globals.account2.clear()
        globals.rules.clear()
        globals.return_to_login.append(True)
        