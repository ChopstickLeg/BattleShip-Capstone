import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from Core.Data import globals

class EndgameScreen(UII):   
    def add_elements(self):
        self.endgame_screen = pygame_menu.Menu("Game Over", globals.resx[0], globals.resy[0], theme = pygame_menu.themes.THEME_BLUE)
        self.endgame_screen.add.label("Game Over, " + globals.game_winner[0].user + " won!")
        self.endgame_screen.add.button("Rematch", self.rematch)
        self.endgame_screen.add.button("Return to login")
        self.endgame_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.endgame_screen.enable()
        self.run_screen(self.endgame_screen)
    
    def rematch(self):
        globals.game_winner.clear()
        globals.rematch.append(True)
        
    
    def return_to_login(self):
        globals.game_winner.clear()
        globals.account1.clear()
        globals.account2.clear()
        globals.rules.clear()
        globals.return_to_login.append(True)
        