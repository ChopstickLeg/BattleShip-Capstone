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
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.KEYDOWN:
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    return
            globals.surface[0].fill(pygame.Color("black"))
            txtLocation = (globals.resx[0] / 2 - 240, globals.resy[0] - 30)
            s = self.font.render("Please switch players now, to dismiss this screen, press any button", True, pygame.Color("white"))
            if self.txt != "":
                s1 = self.font.render(self.txt, True, pygame.Color("white"))
                globals.surface[0].blit(s1, (globals.resx[0] / 2 - 40, globals.resy[0] / 2))
            globals.surface[0].blit(s, txtLocation)
            pygame.display.flip()
            self.clock.tick(60)