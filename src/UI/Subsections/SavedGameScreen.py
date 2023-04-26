import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from Core.Services import SavedGameService
import sys

class SavedGamesScreen(UII):
    def add_elements(self):
        self.saved_games_screen = pygame_menu.Menu("Select a saved game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        service = SavedGameService()
        game_list = service.get_saved_games()
        #Implement droplist here for game saves
        buttonlist = []
        for item in game_list:

        self.table = self.saved_games_screen.add.table()
        self.saved_games_screen.add.button("Next screen", self.build_gameplay_screen)
        self.on_resize(self.saved_games_screen)
        self.saved_games_screen.enable()
        self.run_screen(self.saved_games_screen)
    
    def build_gameplay_screen(self):
        messagebox.showerror(title="Not yet implmented", message="This screen has not yet been fully implemented, the program will now exit")
        sys.exit()