import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen

class ShipPlacementScreen(UII):
    def __init__(self, service, surface):
        super().__init__(service, surface)
    def add_elements(self):
        self.ship_placement_screen = pygame_menu.Menu("Place your ships", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.table1 = self.ship_placement_screen.add.table(border_color = "black")
        for n in range(10):
            self.table1.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
        self.ship_placement_screen.add.button("Next Screen", self.build_gameplay_screen)
        self.on_resize(self.ship_placement_screen)
        self.ship_placement_screen.enable()
        self.run_screen(self.ship_placement_screen)
    
    def build_gameplay_screen(self):
        self.gameplay_screen = GameplayScreen(self.accountService, self.surface)
        self.gameplay_screen.add_elements()