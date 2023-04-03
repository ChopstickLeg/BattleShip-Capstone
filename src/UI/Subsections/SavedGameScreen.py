import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
import sys

class SavedGamesScreen(UII):
    def add_elements(self):
        self.saved_games_screen = pygame_menu.Menu("Select a saved game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.saved_games_screen.add.button("Saved game from <time> with players <player1> <player2>")
        self.saved_games_screen.add.button("Next screen", self.build_gameplay_screen)
        self.on_resize(self.saved_games_screen)
        self.saved_games_screen.enable()
        self.run_screen(self.saved_games_screen)
    
    def build_gameplay_screen(self):
        messagebox.showerror(title="Not yet implmented", message="This screen has not yet been fully implemented, the program will now exit")
        sys.exit()