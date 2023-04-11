import pygame
import pygame_widgets
from pygame_widgets.button import Button
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen
from .TransitionScreen import TransitionScreen
from Core.Data import globals

class GameplayScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.clock = pygame.time.Clock()
        self.board1_surf = self.create_board_surf()
        self.board2_surf = self.create_board_surf()
        self.resx, self.resy = globals.surface[0].get_size()
        self.border = 50
        self.num = self.board.size
        self.tile_size = self.calculate_tile_size()
        self.board1pos = [(self.resx / 4) - self.tile_size * (self.num / 2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.board2pos = [(self.resx / 4 * 3) - self.tile_size * (self.num/2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.titleFont = pygame.font.SysFont("", 60)
        self.font = pygame.font.SysFont("", 32)
        self.selected_square1 = None
        self.selected_square2 = None
    
    def calculate_tile_size(self):
        tSize = (self.resx / 2 - self.border * 2 - 100) / self.num
        if tSize > 70:
            return 70
        else:
            return tSize

    def create_board_surf(self):
        board_surf = pygame.surface.Surface(self.tile_size * self.num, self.tile_size * self.num)
        board_surf.fill(pygame.Color("white"))
        for y in range(self.num):
            for x in range(self.num):
                rect = pygame.rect.Rect(x * self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(board_surf, pygame.Color("black"), rect, 2)
        return board_surf
    
    def get_square_under_mouse(self, board):
        mouse_pos1 = pygame.Vector2(pygame.mouse.get_pos()) - self.board1pos
        mouse_pos2 = pygame.Vector2(pygame.mouse.get_pos()) - self.board2pos
        x1, y1 = [int(v // self.tile_size) for v in mouse_pos1]
        x2, y2 = [int(v // self.tile_size) for v in mouse_pos2]
        try: 
            if x1 >= 0 and y1 >= 0: return (board[y1][x1], x1, y1)
        except IndexError:
            try:
                if x2 >= 0 and y2 >= 0: return (board[y2][x2], x2, y2)
            except IndexError:pass
        return None, None, None
    
    
    def add_elements(self):
        self.run_screen()
    
    def run_screen(self):
        while True:
            ship, x, y = self.get_square_under_mouse(self.board.board1)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.MOUSEBUTTONUP:
                    if self.selected_ship != None:
                        if ship == -1:
                            self.selected_square = ship, x, y

                    
            globals.surface[0].fill((228, 230, 246))
            globals.surface[0].blit(self.board1_surf, self.board1pos)
            globals.surface[0].blit(self.board2_surf, self.board2pos)

            s = self.titleFont.render("Destroy the enemy", True, pygame.Color("black"))
            s2 = self.titleFont.render("Destroy the enemy", True, pygame.Color("darkgrey"))
            globals.surface[0].blit(s2, (1, 1))
            globals.surface[0].blit(s, (0, 0))
            
            self.drawships()
            self.drawhits()
            pygame_widgets.update(events)
            pygame.display.update()

            pygame.display.flip()
            self.clock.tick(60)
            self.selected_square = None
    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen()
        self.pause_screen.add_elements()