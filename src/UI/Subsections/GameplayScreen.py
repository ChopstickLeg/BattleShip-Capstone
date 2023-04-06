import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen
from Core.Data import globals

class GameplayScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.table2_contents = []
        self.table3_contents = []
    
    def add_elements(self):
        self.gameplay_screen = pygame_menu.Menu("Play the game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.table2 = self.gameplay_screen.add.table(border_color = "black")
        self.table3 = self.gameplay_screen.add.table(border_color = "black")
        for n in range(self.board.size):
            for i in self.board.board1[n]:
                if i == -1:
                    self.table2_contents.append("\t")
                else:
                    self.table2_contents.append(str(i))
            self.table2.add_row(self.table2_contents)
            for i in self.board.board2[n]:
                if i == -1:
                    self.table3_contents.append(" ")
                else:
                    self.table3_contents.append(str(i))
            self.table3.add_row(self.table3_contents)
            self.table2_contents = []
            self.table3_contents = []
        self.gameplay_screen.add.button("Next Screen", self.build_pause_screen)
        self.on_resize(self.gameplay_screen)
        self.gameplay_screen.enable()
        self.run_screen(self.gameplay_screen)
    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen()
        self.pause_screen.add_elements()