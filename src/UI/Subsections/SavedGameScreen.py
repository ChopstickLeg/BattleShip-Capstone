import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .TransitionScreen import TransitionScreen
from .GameplayScreen import GameplayScreen
from Core.Services.SavedGameService import SavedGameService
import sys
from Core.Data import globals

class SavedGamesScreen(UII):
    def add_elements(self):
        self.return_flag = False
        self.saved_games_screen = pygame_menu.Menu("Select a saved game", globals.resx[0], globals.resy[0], theme = pygame_menu.themes.THEME_BLUE)
        self.service = SavedGameService()
        game_list = self.service.get_saved_games()
        self.value_list = []
        self.dropdown = []
        for item in game_list:
            if globals.account1[0].user == item[1][0] or globals.account1[0].user == item[1][1]:
                self.value_list.append(item)
                self.dropdown.append((item[1][0] + " and " + item[1][1] + " Played at: " + item[1][5] + ":" + item[1][6][:-4] + " on " + item[1][3] + "/" + item[1][4] + "/" + item[1][2], item[0]))
        if len(self.dropdown) == 0:
            self.saved_games_screen.add.label("No saved games to display")
            self.saved_games_screen.add.button("Back", self.swap_flag)
        else:
            self.drop = self.saved_games_screen.add.dropselect("Select a saved game", items=self.dropdown, placeholder="Please select from one of the saved games in the dropdown", selection_box_width = 0)
            self.saved_games_screen.add.button("Resume Game", self.build_gameplay_screen)
            self.saved_games_screen.add.button("Back", self.swap_flag)
        self.saved_games_screen.enable()
        self.run_screen()

    def swap_flag(self):
        self.return_flag = True
    
    def build_gameplay_screen(self):
        value = self.drop.get_value()
        board_params = self.service.load_saved_game(self.value_list[value[1]][1])
        board = self.service.resume_game(board_params[0], board_params[1], board_params[2], board_params[3], board_params[4], board_params[5], board_params[6], board_params[7])
        globals.account2.append(globals.services[0].getAccountByUser(self.value_list[value[1]][1][1]))
        if globals.services[2].isPlayer1:
            tr_screen = TransitionScreen("Player 1, " + str(globals.account1[0].user) + " is first")
            tr_screen.run_screen()
        else:
            tr_screen = TransitionScreen("Player 2, " + str(globals.account2[0].user) + " is first")
        gameplay = GameplayScreen(board)
        gameplay.add_elements()

    def run_screen(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            self.saved_games_screen.update(events)
            self.saved_games_screen.draw(globals.surface[0])
            pygame.display.flip()
            if self.return_flag:
                return