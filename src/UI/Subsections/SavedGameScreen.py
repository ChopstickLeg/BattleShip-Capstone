import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from Core.Services.SavedGameService import SavedGameService
import sys
from Core.Data import globals

class SavedGamesScreen(UII):
    def add_elements(self):
        self.saved_games_screen = pygame_menu.Menu("Select a saved game", globals.resx[0], globals.resy[0], theme = pygame_menu.themes.THEME_BLUE)
        service = SavedGameService()
        game_list = service.get_saved_games()
        #Implement droplist here for game saves
        dropdown = []
        for item in game_list:
            dropdown.append((item[1][0] + " and " + item[1][1] + " Played at: " + item[1][5] + ":" + item[1][6] + " on " + item[1][3] + "/" + item[1][4] + "/" + item[1][2], item[0]))
        if len(dropdown) == 0:
            self.saved_games_screen.add.label("No saved games to display")
        else:
            self.drop = self.saved_games_screen.add.dropselect("Select a saved game", items=dropdown)

        self.saved_games_screen.add.button("Next screen", self.build_gameplay_screen)
        self.saved_games_screen.enable()
        self.run_screen(self.saved_games_screen)
    
    def build_gameplay_screen(self):
        messagebox.showerror(title="Not yet implmented", message="This screen has not yet been fully implemented, the program will now exit")
        sys.exit()