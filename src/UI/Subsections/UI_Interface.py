from abc import ABC, abstractmethod
import pygame
import pygame_menu
from tkinter import messagebox

class UI_Interface(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    
    def run_screen(self, menu):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.on_resize(menu)
            menu.update(events)
            menu.draw(self.surface)
            pygame.display.flip()
    
    def on_resize(self, menu):
        windowSize = self.surface.get_size()
        newW, newH = windowSize[0], windowSize[1]
        menu.resize(newW, newH)