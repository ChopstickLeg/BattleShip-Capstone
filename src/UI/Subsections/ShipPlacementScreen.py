import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray
from functools import partial
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from Core.Data import globals
from pygame.locals import *

class ShipPlacementScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.isBoard2 = False
        self.resx, self.resy = globals.surface[0].get_size()
        self.smallest = self.get_smallest()
        self.border = 50
        self.num = board.size
        self.tile_size = self.calculate_tile_size()
        self.board_pos = [(self.resx / 2) - self.tile_size * (self.num / 2), (self.resy / 2) - self.tile_size * (self.num / 2) - 50]
        self.button_pos = [self.board_pos[0], self.resy / 2 + (self.tile_size * (self.num / 2)) - 50]
        self.font = pygame.font.SysFont('', 32)
        self.ship_button_txt = self.get_ship_button_txt()
        self.ship_button_fn_list = self.get_ship_fn()
        self.ship_button_list = []
        self.board_surf = self.create_board_surf()
        self.button_surf = self.create_button_surf(board)
        self.clock = pygame.time.Clock()
        self.selected_ship = None
        self.selected_square = None
        self.ship_count = [0 for i in range(len(board.ship_list))]
        self.last_placed = ()
        self.drop_pos = None
    
    def add_elements(self):
        self.run_screen()
    
    def get_smallest(self):
        if self.resx >= self.resy:
            return self.resy
        else:
            return self.resx
    
    def calculate_tile_size(self):
        tSize = (self.smallest - self.border * 2 - 100) / self.num
        if tSize > 70:
            return 70
        else:
            return tSize

    def get_ship_button_txt(self):
        tmp = []
        for i in range(len(self.board.ship_list)):
            tmp.append("Ship " + str(i + 1) + " length: " + str(self.board.ship_list[i]))
        return tuple(tmp)
    def get_ship_fn(self):
        tmp = []
        for i in range(len(self.board.ship_list)):
            tmp.append(partial(self.change_selected, i))
        return tuple(tmp)

    def create_board_surf(self):
        board_surf = pygame.surface.Surface((self.tile_size * self.num, self.tile_size * self.num))
        board_surf.fill(pygame.Color("white"))
        for y in range(self.num):
            for x in range(self.num):
                rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(board_surf, pygame.Color('black'), rect, 2)
        return board_surf
    
    def create_button_surf(self, board):
        button_surf = pygame.surface.Surface((self.resx, self.resy))
        button_surf.fill((228, 230, 246))
        self.ship_button_list = ButtonArray(button_surf, self.button_pos[0], self.button_pos[1], self.tile_size * self.num, 100, (len(self.board.ship_list), 1), border = 10, texts = self.ship_button_txt,
                                            onClicks = self.ship_button_fn_list)
        self.exit_button = Button(button_surf, self.resx - 100, 0, 100, 100, text = "X", onClick = lambda: quit())
        self.next_screen = Button(button_surf, self.resx - 100, self.resy - 100, 100, 100, text = "Next", onClick = self.build_next_screen)
        self.reset_board_button = Button(button_surf, 0, self.resy - 100, 100, 100, text = "Reset Board", onClick = self.reset_board)
        return button_surf
    
    def change_selected(self, num):
        self.selected_ship = num
        print(num)
    
    def reset_board(self):
        if self.isBoard2:
            self.board.board2 = [[-1 for x in range(self.num)] for i in range(self.num)]
        else:
            self.board.board1 = [[-1 for x in range(self.num)] for i in range(self.num)]
        self.ship_count = [0 for i in range(len(self.board.ship_list))]
        self.last_placed = ()
    
    def get_square_under_mouse(self, board):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.board_pos
        x, y = [int(v // self.tile_size) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (board[y][x], x, y)
        except IndexError: pass
        return None, None, None

    def draw_ship(self, board):
        sx, sy = None, None
        if self.selected_square:
            square, sx, sy = self.selected_square
            if square == -1:
                if not globals.services[1].verify_placement(board, sx, sy, self.last_placed, self.ship_count[self.selected_ship], self.board.ship_list[self.selected_ship], self.selected_ship):
                    messagebox.showerror("Ship placed improperly", "Ship has been placed in an invalid location, please try again")
                    return
                else:
                    board[sx][sy] = self.selected_ship
                    self.ship_count[self.selected_ship] += 1
                    self.last_placed = (sx, sy)
        for x in range(self.num):
            for y in range(self.num):
                if board[x][y] != -1:
                    s1 = self.font.render("s" + str(board[x][y] + 1), True, pygame.Color("black"))
                    s2 = self.font.render("s" + str(board[x][y] + 1), True, pygame.Color("darkgrey"))
                    pos = pygame.Rect(self.board_pos[0] + x * self.tile_size+1, self.board_pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    globals.surface[0].blit(s2, s2.get_rect(center = pos.center).move(1, 1))
                    globals.surface[0].blit(s1, s1.get_rect(center = pos.center))
        return board


    def draw_selector(self, screen, ship, x, y):
        if ship != None:
            rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
    
    def add_instructions(self, screen):
        s = self.font.render("Click a button at the bottom", True, pygame.Color("black"))
        pos = pygame.Rect((self.resx / 2) - 200, self.board_pos[1] - 100, 400, 100)
        screen.blit(s, s.get_rect(center = pos.center))
    
    def add_click_instructions(self, screen):
        s = self.font.render("Now click on a square to place your ship", True, pygame.Color("black"))
        pos = pygame.Rect((self.resx / 2) - 200, self.board_pos[1] - 100, 400, 100)
        screen.blit(s, s.get_rect(center = pos.center))

    def build_next_screen(self):
        ship_totals = [0 for i in range(len(self.board.ship_list))]
        if self.isBoard2:
            for x in range(self.num):
                for y in range(self.num):
                    if self.board.board2[x][y] != -1:
                        ship_totals[self.board.board2[x][y]] += 1
        else:
            for x in range(self.num):
                for y in range(self.num):
                    if self.board.board1[x][y] != -1:
                        ship_totals[self.board.board1[x][y]] += 1
        for i in range(len(ship_totals)):
            if ship_totals[i] != self.board.ship_list[i]:
                messagebox.showerror("Not enough ships placed", "Please place all ships before continuing")
                self.run_screen()
        if len(globals.account2) == 1 and not self.isBoard2:
            self.isBoard2 = True
            self.ship_count = [0 for i in range(len(self.board.ship_list))]
            self.last_placed = ()
            self.run_screen()
        else:
            gameplay_screen = GameplayScreen(self.board)
            gameplay_screen.add_elements()

    
    def run_screen(self):
        while True:
            if self.isBoard2:
                ship, x, y = self.get_square_under_mouse(self.board.board2)
            else:
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

                    
            globals.surface[0].fill(pygame.Color('grey'))
            globals.surface[0].blit(self.button_surf, [0, 0])
            globals.surface[0].blit(self.board_surf, self.board_pos)
            if self.selected_ship != None:
                self.draw_selector(globals.surface[0], ship, x, y)
                self.add_click_instructions(globals.surface[0])
            else:
                self.add_instructions(globals.surface[0])
            if self.isBoard2:
                self.draw_ship(self.board.board2)
            else:
                self.draw_ship(self.board.board1)
            pygame_widgets.update(events)
            pygame.display.update()

            pygame.display.flip()
            self.clock.tick(60)
            self.selected_square = None