import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen

class GameplayScreen(UII):
    def __init__(self, service, surface):
        super().__init__(service, surface)
    
    def add_elements(self):
        self.gameplay_screen = pygame_menu.Menu("Play the game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.table2 = self.gameplay_screen.add.table(border_color = "black")
        self.table3 = self.gameplay_screen.add.table(border_color = "black")
        for n in range(10):
            self.table2.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
            self.table3.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
        self.gameplay_screen.add.button("Next Screen", self.build_pause_screen)
        self.on_resize(self.gameplay_screen)
        self.gameplay_screen.enable()
        self.run_screen(self.gameplay_screen)
    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen(self.accountService, self.surface)
        self.pause_screen.add_elements()