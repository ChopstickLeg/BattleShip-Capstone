from abc import ABC, abstractmethod
import pygame
import pygame_menu
from tkinter import messagebox
from Core.Data import globals

class UI_Interface(ABC):
    def __init__(self):
        pass
    
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
    
    def on_resize(self, menu):
        windowSize = globals.surface[0].get_size()
        newW, newH = windowSize[0], windowSize[1]
        menu.resize(newW, newH)