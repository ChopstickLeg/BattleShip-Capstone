import pygame
import pygame_widgets
from pygame_widgets.button import Button
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen
from .TransitionScreen import TransitionScreen
from Core.Data import globals
import random

class GameplayScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.clock = pygame.time.Clock()
        self.resx, self.resy = globals.surface[0].get_size()
        self.border = 50
        self.num = self.board.size
        self.tile_size = self.calculate_tile_size()
        self.board1pos = [(self.resx / 4) - self.tile_size * (self.num / 2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.board2pos = [(self.resx / 4 * 3) - self.tile_size * (self.num/2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.titleFont = pygame.font.SysFont("", 60)
        self.font = pygame.font.SysFont("", 32)
        self.selected_ship = None
        self.board1_surf = self.create_board_surf()
        self.board2_surf = self.create_board_surf()
        if random.randint(0, 1) == 0:
            self.isPlayer1 = True


    def calculate_tile_size(self):
        tSize = (self.resx / 2 - self.border * 2 - 100) / self.num
        if tSize > 70:
            return 70
        else:
            return tSize

    def create_board_surf(self):
        board_surf = pygame.surface.Surface((self.tile_size * self.num, self.tile_size * self.num))
        board_surf.fill(pygame.Color("white"))
        for y in range(self.num):
            for x in range(self.num):
                rect = pygame.rect.Rect(x * self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(board_surf, pygame.Color("black"), rect, 2)
        return board_surf
    
    def get_square_under_mouse(self, board):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.board2pos
        x, y = [int(v // self.tile_size) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (board[y][x], x, y)
        except IndexError:pass
        return None, None, None
    
    def draw_selector(self, screen, ship, x, y):
        if ship != None:
            rect = (self.board2pos[0] + x * self.tile_size, self.board2pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
    
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
            
            self.draw_selector(globals.surface[0], ship, x, y)
            if self.isPlayer1:
                self.draw_ships(self.board.board1)
                self.draw_hits(self.board.board1)
            else:
                self.draw_ships(self.board.board2)
            
            
            pygame_widgets.update(events)
            pygame.display.update()

            pygame.display.flip()
            self.clock.tick(60)
            self.selected_square = None

    def draw_ships(self, board):
        for x in range(self.num):
            for y in range(self.num):
                if board[y][x] != -1:
                    s1 = self.font.render("s" + str(board[y][x] + 1), True, pygame.Color("black"))
                    s2 = self.font.render("s" + str(board[y][x] + 1), True, pygame.Color("darkgrey"))
                    pos = pygame.Rect(self.board1pos[0] + x * self.tile_size+1, self.board1pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    globals.surface[0].blit(s2, s2.get_rect(center = pos.center).move(1, 1))
                    globals.surface[0].blit(s1, s1.get_rect(center = pos.center))

    def draw_hits(self, shipBoard):
        for x in range(self.num):
            for y in range(self.num):
                if self.board.shotBoard1[y][x] and self.isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    if shipBoard[y][x] != -1:
                        pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                    if shipBoard[y][x] == -1:
                        pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] and self.isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    if shipBoard[y][x] != -1:
                        pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                    if shipBoard[y][x] == -1:
                        pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] and not self.isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    if shipBoard[y][x] != -1:
                        pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                    if shipBoard[y][x] == -1:
                        pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard1[y][x] and not self.isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    if shipBoard[y][x] != -1:
                        pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                    if shipBoard[y][x] == -1:
                        pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)

    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen()
        self.pause_screen.add_elements()