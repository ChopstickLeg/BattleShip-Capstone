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
        self.WHITE = (255, 255, 255)
        self.RED   = (255, 0, 0)
        self.clock = pygame.time.Clock()
        self.resx, self.resy = globals.surface[0].get_size()
        self.tile_size = 32
        self.num = board.size
        self.board_pos = [(self.resx / 2) - self.tile_size * (self.num / 2), (self.resy / 2) - self.tile_size * (self.num / 2)]
        self.font = pygame.font.SysFont('', 32)
        self.board = self.create_board()
        self.board_surf = self.create_board_surf()
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self.drop_pos = None
    
    def add_elements(self):
        self.run_screen()

    def create_board_surf(self):
        board_surf = pygame.surface.Surface((self.tile_size * self.num, self.tile_size * self.num))
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

    def draw_pieces(self, screen, board, font, selected_piece):
        sx, sy = None, None
        if selected_piece:
            piece, sx, sy = selected_piece

        for y in range(self.num):
            for x in range(self.num): 
                piece = board[y][x]
                if piece:
                    selected = x == sx and y == sy
                    color, type = piece
                    s1 = font.render(type[0], True, pygame.Color('red' if selected else color))
                    s2 = font.render(type[0], True, pygame.Color('darkgrey'))
                    pos = pygame.Rect(self.board_pos[0] + x * self.tile_size+1, self.board_pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                    screen.blit(s1, s1.get_rect(center=pos.center))

    def draw_selector(self, screen, piece, x, y):
        if piece != None:
            rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
    
    def draw_drag(self, screen, board, selected_piece, font):
        if selected_piece:
            piece, x, y = self.get_square_under_mouse(board)
            if x != None:
                rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

            color, type = selected_piece[0]
            s1 = font.render(type[0], True, pygame.Color(color))
            s2 = font.render(type[0], True, pygame.Color('darkgrey'))
            pos = pygame.Vector2(pygame.mouse.get_pos())
            screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
            screen.blit(s1, s1.get_rect(center=pos))
            selected_rect = pygame.Rect(self.board_pos[0] + selected_piece[1] * self.tile_size, self.board_pos[1] + selected_piece[2] * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
            return (x, y)

    def on_resize(self, width, height):
        self.resx = width
        self.resy = height
        self.board_pos[0] = (self.resx / 2) - self.tile_size * (self.num / 2)
        self.board_pos[1] = (self.resy / 2) - self.tile_size * (self.num / 2)
        board_surf = self.create_board_surf()
    
    def run_screen(self):
        while True:
            piece, x, y = self.get_square_under_mouse(self.board)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((e.size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.on_resize(e.w, e.h)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece != None:
                        self.selected_piece = piece, x, y
                if e.type == pygame.MOUSEBUTTONUP:
                    if drop_pos:
                        piece, old_x, old_y = self.selected_piece
                        self.board[old_y][old_x] = 0
                        new_x, new_y = drop_pos
                        #errors here if oob
                        self.board[new_y][new_x] = piece
                    self.selected_piece = None
                    drop_pos = None
            globals.surface[0].fill(pygame.Color('grey'))
            globals.surface[0].blit(self.board_surf, self.board_pos)
            self.draw_pieces(globals.surface[0], self.board, self.font, self.selected_piece)
            self.draw_selector(globals.surface[0], piece, x, y)
            drop_pos = self.draw_drag(globals.surface[0], self.board, self.selected_piece, self.font)

            pygame.display.flip()
            self.clock.tick(60)