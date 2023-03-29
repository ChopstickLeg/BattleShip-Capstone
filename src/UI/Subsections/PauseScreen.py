import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .EndgameScreen import EndgameScreen

class PauseScreen(UII):
    def __init__(self, service, surface):
        super().__init__(service, surface)
    
    def add_elements(self):
        self.pause_screen = pygame_menu.Menu("Game Paused", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.pause_screen.add.button("Resume game")
        self.pause_screen.add.button("Save & quit")
        self.pause_screen.add.button("Next Screen", self.build_endgame_screen)
        self.pause_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.pause_screen)
        self.pause_screen.enable()
        self.run_screen(self.pause_screen)
    
    def build_endgame_screen(self):
        self.endgame_screen = EndgameScreen(self.accountService, self.surface)
        self.endgame_screen.add_elements()