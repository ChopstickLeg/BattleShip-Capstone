import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII

class EndgameScreen(UII):
    def __init__(self, service, surface):
        super().__init__(service, surface)
    
    def add_elements(self):
        self.endgame_screen = pygame_menu.Menu("Game Over", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.endgame_screen.add.button("Rematch")
        self.endgame_screen.add.button("Return to login")
        self.endgame_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.endgame_screen)
        self.endgame_screen.enable()
        self.run_screen(self.endgame_screen)