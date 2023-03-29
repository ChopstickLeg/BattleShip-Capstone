import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .ShipPlacementScreen import ShipPlacementScreen
import sqlite3

class RuleSelectionScreen(UII):
    def __init__(self, service, surface):
        super().__init__(service, surface)
    def add_elements(self):
        self.rule_selection_screen = pygame_menu.Menu("Select Your Rules", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.logged_in1, self.logged_in2 = self.accountService.get_logged_in()
        if self.logged_in2 != None:
            self.rule_selection_screen.add.label("Logged in users: " + self.logged_in1.user[0][0] + " " + self.logged_in2.user[0][0])
        else:
            self.rule_selection_screen.add.label("Logged in user: " + self.logged_in1.user[0][0])
        self.rule_selection_screen.add.dropselect(title = "Select Board Size", items = [('7 x 7',), ("8 x 8", ), ('9 x 9',), ('10 x 10', ), ('11 x 11', ), ('12 x 12', ), ('13 x 13', )])
        self.rule_selection_screen.add.dropselect(title = "Select number of 5 length ships", items = ["1", "2", "3"])
        self.rule_selection_screen.add.dropselect(title = "Select number of 4 length ships", items = ["1", "2", "3", "4"])
        self.rule_selection_screen.add.dropselect(title = "Select number of 3 length ships", items = ["1", "2", "3", "4", "5"])
        self.rule_selection_screen.add.dropselect(title = "Select numebr of 2 length ships", items = ["1", "2", "3", "4", "5", "6"])
        self.salvo_toggle = self.rule_selection_screen.add.toggle_switch(title="Salvo Mode")
        self.chain_toggle = self.rule_selection_screen.add.toggle_switch(title="Chain hits")
        self.rule_selection_screen.add.button("Next Screen", self.build_ship_placement_screen)
        self.rule_selection_screen.add.button("Exit Application", pygame_menu.events.EXIT)
        self.on_resize(self.rule_selection_screen)
        self.rule_selection_screen.enable()
        self.run_screen(self.rule_selection_screen)

    def build_ship_placement_screen(self):
        self.ship_placement_screen = ShipPlacementScreen(self.accountService, self.surface)
        self.ship_placement_screen.add_elements()

    def check_salvo_mode(self):
        #set value from chain toggle, then disable it accordingly
        pass