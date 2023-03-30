import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen
from Core.Data import globals

class GameplayScreen(UII):
    def __init__(self, service, service2, surface):
        super().__init__(service, service2, surface)
    
    def add_elements(self):
        self.gameplay_screen = pygame_menu.Menu("Play the game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.table2 = self.gameplay_screen.add.table(border_color = "black")
        self.table3 = self.gameplay_screen.add.table(border_color = "black")
        for n in range(globals.board[0].size):
            self.table2.add_row(["\t" for i in range(globals.board[0].size)])
            self.table3.add_row(["\t" for i in range(globals.board[0].size)])
        self.gameplay_screen.add.button("Next Screen", self.build_pause_screen)
        self.on_resize(self.gameplay_screen)
        self.gameplay_screen.enable()
        self.run_screen(self.gameplay_screen)
    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen(self.accountService, self.boardService, self.surface)
        self.pause_screen.add_elements()