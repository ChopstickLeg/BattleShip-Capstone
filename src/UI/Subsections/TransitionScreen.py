import pygame
from .UI_Interface import UI_Interface as UII
from Core.Data import globals

class TransitionScreen(UII):
    def __init__(self, txt = ""):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("", 32)
        self.titleFont = pygame.font.SysFont("", 60)
        self.txt = txt
    def run_screen(self):
        pygame.time.wait(2000)
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.KEYUP:
                    return
                if e.type == pygame.MOUSEBUTTONUP:
                    return
            globals.surface[0].fill(pygame.Color("black"))
            resx, resy = globals.surface[0].get_size()
            txtLocation = (resx / 2 - 100, resy - 40)
            s = self.font.render("Please switch players now, to dismiss this screen, press any button", True, pygame.Color("white"))
            if self.txt != "":
                s1 = self.font.render(self.txt, True, pygame.Color("white"))
                globals.surface.blit(s1, resx / 2 - 50, resy / 2)
            globals.surface[0].blit(s, txtLocation)
            pygame.display.flip()
            self.clock.tick(60)