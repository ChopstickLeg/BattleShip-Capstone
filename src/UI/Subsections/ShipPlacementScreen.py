import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from Core.Data import globals

class ShipPlacementScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
    def add_elements(self):
        self.ship_placement_screen = pygame_menu.Menu("Place your ships", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.table1 = self.ship_placement_screen.add.table(border_color = "black")
        for n in range(self.board.size):
            self.table1.add_row(["\t" for i in range(self.board.size)])
        self.ship_placement_screen.add.button("Next Screen", self.build_gameplay_screen)
        self.on_resize(self.ship_placement_screen)
        self.ship_placement_screen.enable()
        self.run_screen(self.ship_placement_screen)
    
    def build_gameplay_screen(self):
        self.gameplay_screen = GameplayScreen(self.board)
        self.gameplay_screen.add_elements()