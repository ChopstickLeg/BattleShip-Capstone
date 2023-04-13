import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from Core.Data import globals

class PauseScreen(UII):
    def __init__(self):
        super().__init__()
        self.return_flag = False
    def add_elements(self):
        self.pause_screen = pygame_menu.Menu("Game Paused", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.pause_screen.add.button("Resume game", self.swap_flag)
        self.pause_screen.add.button("Save & quit")
        self.pause_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.pause_screen)
        self.pause_screen.enable()
        self.run_screen(self.pause_screen)
    def swap_flag(self):
        self.return_flag = True
    def run_screen(self, menu):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            menu.update(events)
            menu.draw(globals.surface[0])
            pygame.display.flip()
            if self.return_flag:
                return