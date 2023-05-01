import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from Core.Data import globals
from Core.Services.SavedGameService import SavedGameService
import sys

class PauseScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.return_flag = False
        self.board = board
        self.sgs = SavedGameService()
    def add_elements(self):
        self.pause_screen = pygame_menu.Menu("Game Paused", globals.resx[0], globals.resy[0], theme=pygame_menu.themes.THEME_BLUE)
        self.pause_screen.add.button("Resume game", self.swap_flag)
        self.pause_screen.add.button("Save & quit", self.save_game)
        self.pause_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.pause_screen.enable()
        self.run_screen()
    def swap_flag(self):
        self.return_flag = True
    def save_game(self):
        self.sgs.save_game(self.board)
        sys.exit(0)
    def run_screen(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            self.pause_screen.update(events)
            self.pause_screen.draw(globals.surface[0])
            pygame.display.flip()
            if self.return_flag:
                return