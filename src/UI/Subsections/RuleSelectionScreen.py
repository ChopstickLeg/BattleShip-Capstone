import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .ShipPlacementScreen import ShipPlacementScreen
from Core.Data import globals

class RuleSelectionScreen(UII):
    def __init__(self):
        super().__init__()
        self.board = None
    def add_elements(self):
        self.rule_selection_screen = pygame_menu.Menu("Select Your Rules", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        if len(globals.account2) == 1:
            self.rule_selection_screen.add.label("Logged in users: " + globals.account1[0].user + " " + globals.account2[0].user)
        else:
            self.rule_selection_screen.add.label("Logged in user: " + globals.account1[0].user)
        self.board_size = self.rule_selection_screen.add.dropselect(title = "Select Board Size", items = [('7 x 7', 7), ("8 x 8", 8), ('9 x 9', 9), ('10 x 10', 10), ('11 x 11', 11), ('12 x 12', 12), ('13 x 13', 13)])
        #add restrictions to these based on board size?
        self.ship5 = self.rule_selection_screen.add.dropselect(title = "Select number of 5 length ships", items = ["1", "2", "3"])
        self.ship4 = self.rule_selection_screen.add.dropselect(title = "Select number of 4 length ships", items = ["1", "2", "3", "4"])
        self.ship3 = self.rule_selection_screen.add.dropselect(title = "Select number of 3 length ships", items = ["1", "2", "3", "4", "5"])
        self.ship2 = self.rule_selection_screen.add.dropselect(title = "Select numebr of 2 length ships", items = ["1", "2", "3", "4", "5", "6"])
        self.salvo_toggle = self.rule_selection_screen.add.toggle_switch(title="Salvo Mode", onchange=self.check_salvo_mode)
        self.chain_toggle = self.rule_selection_screen.add.toggle_switch(title="Chain hits", onchange=self.check_chain_mode)
        self.rule_selection_screen.add.button("Place your ships", self.create_board)
        self.rule_selection_screen.add.button("Exit Application", pygame_menu.events.EXIT)
        self.on_resize(self.rule_selection_screen)
        self.rule_selection_screen.enable()
        self.run_screen(self.rule_selection_screen)

    def build_ship_placement_screen(self):
        self.ship_placement_screen = ShipPlacementScreen(self.board)
        self.ship_placement_screen.add_elements()

    def check_salvo_mode(self, state):
        if state:
            self.chain_toggle.set_value(False)
            self.chain_toggle.set_controls(mouse = False, keyboard = False)
        else:
            self.chain_toggle.set_controls(mouse = True, keyboard = True)
    
    def check_chain_mode(self, state):
        if state:
            self.salvo_toggle.set_value(False)
            self.salvo_toggle.set_controls(mouse = False, keyboard = False)
        else:
            self.salvo_toggle.set_controls(mouse = True, keyboard = True)
    
    def create_board(self):
        try:
            board_size = self.board_size.get_value()
            ship5 = self.ship5.get_value()
            ship4 = self.ship4.get_value()
            ship3 = self.ship3.get_value()
            ship2 = self.ship2.get_value()
        except ValueError:
            messagebox.showerror(title="Not all fields selected", message="Please select a value from all dropdowns")
            self.run_screen(self.rule_selection_screen)
        salvo = self.salvo_toggle.get_value()
        chain = self.chain_toggle.get_value()
        ship5 = int(ship5[0])
        ship4 = int(ship4[0])
        ship3 = int(ship3[0])
        ship2 = int(ship2[0])
        try:
            self.board = globals.services[1].generate_board(board_size[0][1], ship5, ship4, ship3, ship2, globals.account1[0], globals.account2[0], salvo, chain)
        except IndexError:
            self.board = globals.services[1].generate_board(size = board_size[0][1], ship5 = ship5, ship4 = ship4, ship3 = ship3, ship2 = ship2, player1 = globals.account1[0], salvo = salvo, chain = chain)
        self.build_ship_placement_screen()