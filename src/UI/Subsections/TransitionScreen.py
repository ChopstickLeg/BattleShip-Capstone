import pygame
from .UI_Interface import UI_Interface as UII
from Core.Data import globals

class TransitionScreen(UII):
    def __init__(self):
        super.__init__()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("", 32)
    def run_screen(self):
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.KEYUP:
                    return
                if e.type == pygame.MOUSEBUTTONUP:
                    return
            globals.surface[0].fill(pygame.Color("black"))
            resx, resy = globals.surface[0].get_size()
            txtLocation = (resx / 2 - 150, resy / 2 - 100)
            s = self.font.render("Please switch players now, to dismiss this screen, press any button", True, pygame.Color("white"))
            globals.surface[0].blit(s, txtLocation)
            pygame.display.flip()
            self.clock.tick(60)