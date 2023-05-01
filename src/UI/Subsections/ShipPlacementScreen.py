import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray
from functools import partial
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .GameplayScreen import GameplayScreen
from .TransitionScreen import TransitionScreen
from Core.Data import globals
from pygame.locals import *

class ShipPlacementScreen(UII):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.isBoard2 = False
        self.smallest = self.get_smallest()
        self.border = 50
        self.num = board.size
        self.tile_size = self.calculate_tile_size()
        self.board_pos = [(globals.resx[0] / 2) - self.tile_size * (self.num / 2), (globals.resy[0] / 2) - self.tile_size * (self.num / 2) - 50]
        self.button_pos = [self.board_pos[0], globals.resy[0] / 2 + (self.tile_size * (self.num / 2)) - 50]
        self.titleFont = pygame.font.SysFont("", 60)
        self.font = pygame.font.SysFont('', 32)
        self.ship_button_txt = self.get_ship_button_txt()
        self.ship_button_fn_list = self.get_ship_fn()
        self.buttons_wide, self.buttons_long = self.calculate_button_nums()
        self.ship_button_list = []
        self.board_surf = self.create_board_surf()
        self.button_surf = self.create_button_surf()
        self.clock = pygame.time.Clock()
        self.selected_ship = None
        self.selected_square = None
        self.ship_count = [0 for i in range(len(board.ship_list))]
        self.last_placed = ()
    
    def add_elements(self):
        self.run_screen()
    
    def calculate_button_nums(self):
        if len(self.board.ship_list) > 5:
            wide = 2
            long = len(self.board.ship_list) // 2 + len(self.board.ship_list) % 2
        else:
            wide = 1
            long = len(self.board.ship_list)
        return wide, long
    
    def get_smallest(self):
        if globals.resx[0] >= globals.resy[0]:
            return globals.resy[0]
        else:
            return globals.resx[0]
    
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
        if len(self.board.ship_list) > 5 and len(self.board.ship_list) % 2 != 0:
            tmp.append("Placeholder, do not click")
        return tuple(tmp)
    def get_ship_fn(self):
        tmp = []
        for i in range(len(self.board.ship_list)):
            tmp.append(partial(self.change_selected, i))
        if len(self.board.ship_list) > 5 and len(self.board.ship_list) % 2 != 0:
            tmp.append(partial(self.change_selected, None))
        return tuple(tmp)

    def create_board_surf(self):
        board_surf = pygame.surface.Surface((self.tile_size * self.num, self.tile_size * self.num))
        board_surf.fill(pygame.Color("white"))
        for y in range(self.num):
            for x in range(self.num):
                rect = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(board_surf, pygame.Color('black'), rect, 2)
        return board_surf
    
    def create_button_surf(self):
        button_surf = pygame.surface.Surface((globals.resx[0], globals.resy[0]))
        button_surf.fill((228, 230, 246))
        #Fix index error for odd number of ships here
        self.ship_button_list = ButtonArray(button_surf, self.button_pos[0], self.button_pos[1], self.tile_size * self.num, 100, (self.buttons_long, self.buttons_wide), border = 10, texts = self.ship_button_txt,
                                            onClicks = self.ship_button_fn_list)
        self.exit_button = Button(button_surf, globals.resx[0] - 50, 0, 50, 50, text = "X", onClick = lambda: quit())
        self.next_screen = Button(button_surf, globals.resx[0] - 100, globals.resy[0] - 50, 100, 50, text = "Next", onClick = self.build_next_screen)
        self.reset_board_button = Button(button_surf, 0, globals.resy[0] - 50, 100, 50, text = "Reset Board", onClick = self.reset_board)
        return button_surf
    
    def change_selected(self, num):
        self.selected_ship = num
    
    def reset_board(self):
        if self.isBoard2:
            self.board.board2 = [[0 for x in range(self.num)] for i in range(self.num)]
        else:
            self.board.board1 = [[0 for x in range(self.num)] for i in range(self.num)]
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
            if square == 0:
                if not globals.services[1].verify_placement(board, sy, sx, self.last_placed, self.ship_count[self.selected_ship], self.board.ship_list[self.selected_ship], self.selected_ship):
                    messagebox.showerror("Ship placed improperly", "Ship has been placed in an invalid location, please try again")
                    return
                else:
                    board[sy][sx] = self.selected_ship + 1
                    self.ship_count[self.selected_ship] += 1
                    self.last_placed = (sy, sx)
        for x in range(self.num):
            for y in range(self.num):
                if board[y][x] != 0:
                    s1 = self.font.render("s" + str(board[y][x]), True, pygame.Color("black"))
                    s2 = self.font.render("s" + str(board[y][x]), True, pygame.Color("darkgrey"))
                    pos = pygame.Rect(self.board_pos[0] + x * self.tile_size+1, self.board_pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    globals.surface[0].blit(s2, s2.get_rect(center = pos.center).move(1, 1))
                    globals.surface[0].blit(s1, s1.get_rect(center = pos.center))
        return board


    def draw_selector(self, ship, x, y):
        if ship != None:
            rect = (self.board_pos[0] + x * self.tile_size, self.board_pos[1] + y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(globals.surface[0], (255, 0, 0, 50), rect, 2)
    
    def add_instructions(self):
        s = self.font.render("Click a button at the bottom", True, pygame.Color("black"))
        pos = pygame.Rect((globals.resx[0] / 2) - 200, self.board_pos[1] - 100, 400, 100)
        globals.surface[0].blit(s, s.get_rect(center = pos.center))
    
    def add_click_instructions(self):
        s = self.font.render("Now click on a square to place your ship", True, pygame.Color("black"))
        pos = pygame.Rect((globals.resx[0] / 2) - 200, self.board_pos[1] - 100, 400, 100)
        globals.surface[0].blit(s, s.get_rect(center = pos.center))

    def build_next_screen(self):
        ship_totals = [0 for i in range(len(self.board.ship_list))]
        if self.isBoard2:
            for x in range(self.num):
                for y in range(self.num):
                    if self.board.board2[x][y] != 0:
                        ship_totals[self.board.board2[x][y] - 1] += 1
        else:
            for x in range(self.num):
                for y in range(self.num):
                    if self.board.board1[x][y] != 0:
                        ship_totals[self.board.board1[x][y] - 1] += 1
        for i in range(len(ship_totals)):
            if ship_totals[i] != self.board.ship_list[i]:
                messagebox.showerror("Not enough ships placed", "Please place all ships before continuing")
                self.run_screen()
        if globals.services[0].isPVP and not self.isBoard2:
            self.isBoard2 = True
            self.ship_count = [0 for i in range(len(self.board.ship_list))]
            self.last_placed = ()
            self.run_screen()
        elif globals.services[0].isPVP and self.isBoard2:
            if globals.services[2].isPlayer1:
                transitionScreen = TransitionScreen("Player 1 goes first")
            else:
                transitionScreen = TransitionScreen("Player 2 goes first")
            transitionScreen.run_screen()
            gameplay_screen = GameplayScreen(self.board)
            gameplay_screen.add_elements()
        elif not globals.services[0].isPVP:
            self.board.board2 = globals.services[3].place_ships(self.num, self.board.ship_list, self.board.board2)
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
                        if ship == 0:
                            self.selected_square = ship, x, y

                    
            globals.surface[0].fill(pygame.Color('grey'))
            globals.surface[0].blit(self.button_surf, [0, 0])
            globals.surface[0].blit(self.board_surf, self.board_pos)

            s = self.titleFont.render("Place Your Ships", True, pygame.Color("black"))
            s2 = self.titleFont.render("Place Your Ships", True, pygame.Color("darkgrey"))
            globals.surface[0].blit(s2, (1, 1))
            globals.surface[0].blit(s, (0, 0))
            
            if self.selected_ship != None:
                self.draw_selector(ship, x, y)
                self.add_click_instructions()
            else:
                self.add_instructions()
            if self.isBoard2:
                self.draw_ship(self.board.board2)
            else:
                self.draw_ship(self.board.board1)
            pygame_widgets.update(events)
            pygame.display.update()

            pygame.display.flip()
            self.clock.tick(0)
            self.selected_square = None
            if len(globals.rematch) == 1 or len(globals.return_to_login) == 1:
                return