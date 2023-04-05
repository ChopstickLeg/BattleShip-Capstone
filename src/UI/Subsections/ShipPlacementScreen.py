import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from Core.Data import globals
from pygame.locals import *

class ShipPlacementScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.Bboard = board
        self.resx, self.resy = globals.surface[0].get_size()
        self.smallest = self.get_smallest()
        self.border = 50
        self.num = board.size
        self.tile_size = self.calculate_tile_size()
        self.board_pos = [(self.resx / 2) - self.tile_size * (self.num / 2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.font = pygame.font.SysFont('', 32)
        self.board = self.create_board()
        self.board_surf = self.create_board_surf()
        self.clock = pygame.time.Clock()
        self.selected_ship = None
        self.drop_pos = None
        self.ship_total = board.ship5 + board.ship4 + board.ship3 + board.ship2
    
    def add_elements(self):
        self.run_screen()
    
    def get_smallest(self):
        if self.resx >= self.resy:
            return self.resy
        else:
            return self.resx
    
    def calculate_tile_size(self):
        tSize = (self.smallest - self.border * 2) / self.num
        if tSize > 50:
            return tSize
        elif self.smallest < 400:
            messagebox.showerror(title="Window size too small", message="Please increase the size of the window to improve your playing experience")
            return tSize
        else:
            return tSize

    def create_board_surf(self):
        board_surf = pygame.surface.Surface((self.tile_size * self.num, self.tile_size * self.num + 100))
        board_surf.fill(pygame.Color("white"))
        for y in range(self.num):
            for x in range(self.num):
                rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(board_surf, pygame.Color('black'), rect, 2)
        
        return board_surf
    
    def get_square_under_mouse(self, board):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.board_pos
        x, y = [int(v // self.tile_size) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (board[y][x], x, y)
        except IndexError: pass
        return None, None, None

    def create_board(self):
        board = []
        for y in range(self.num):
            board.append([])
            for x in range(self.num):
                board[y].append(None)

        for x in range(0, self.num):
            board[1][x] = ('black', 'pawn')
        for x in range(0, self.num):
            board[6][x] = ('white', 'pawn')
        return board

    def draw_ships(self, screen, board, font, selected_ship):
        sx, sy = None, None
        if selected_ship:
            ship, sx, sy = selected_ship

        for y in range(self.num):
            for x in range(self.num): 
                ship = board[y][x]
                if ship:
                    selected = x == sx and y == sy
                    color, type = ship
                    s1 = font.render(type[0], True, pygame.Color('red' if selected else color))
                    s2 = font.render(type[0], True, pygame.Color('darkgrey'))
                    pos = pygame.Rect(self.board_pos[0] + x * self.tile_size+1, self.board_pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                    screen.blit(s1, s1.get_rect(center=pos.center))

    def draw_selector(self, screen, ship, x, y):
        if ship != None:
            rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
    
    def draw_drag(self, screen, board, selected_ship, font):
        if selected_ship:
            ship, x, y = self.get_square_under_mouse(board)
            if x != None:
                rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

            color, type = selected_ship[0]
            s1 = font.render(type[0], True, pygame.Color(color))
            s2 = font.render(type[0], True, pygame.Color('darkgrey'))
            pos = pygame.Vector2(pygame.mouse.get_pos())
            screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
            screen.blit(s1, s1.get_rect(center=pos))
            selected_rect = pygame.Rect(self.board_pos[0] + selected_ship[1] * self.tile_size, self.board_pos[1] + selected_ship[2] * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
            return (x, y)

    def on_resize(self, width, height):
        self.resx = width
        self.resy = height
        self.board_pos[0] = (self.resx / 2) - self.tile_size * (self.num / 2)
        self.board_pos[1] = (self.resy / 2) - self.tile_size * (self.num / 2)
        self.smallest = self.get_smallest()
        self.tile_size = self.calculate_tile_size()
        self.board_surf = self.create_board_surf()
    
    def run_screen(self):
        while True:
            ship, x, y = self.get_square_under_mouse(self.board)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.VIDEORESIZE:
                    globals.surface[0] = pygame.display.set_mode((e.size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.on_resize(e.w, e.h)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if ship != None:
                        self.selected_ship = ship, x, y
                if e.type == pygame.MOUSEBUTTONUP:
                    if drop_pos:
                        ship, old_x, old_y = self.selected_ship
                        self.board[old_y][old_x] = 0
                        new_x, new_y = drop_pos
                        #errors here if oob
                        self.board[new_y][new_x] = ship
                    self.selected_ship = None
                    drop_pos = None
            globals.surface[0].fill(pygame.Color('grey'))
            globals.surface[0].blit(self.board_surf, self.board_pos)
            self.draw_ships(globals.surface[0], self.board, self.font, self.selected_ship)
            self.draw_selector(globals.surface[0], ship, x, y)
            drop_pos = self.draw_drag(globals.surface[0], self.board, self.selected_ship, self.font)

            pygame.display.flip()
            self.clock.tick(60)