import pygame
import pygame_widgets
from pygame_widgets.button import Button
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .PauseScreen import PauseScreen
from .TransitionScreen import TransitionScreen
from .EndgameScreen import EndgameScreen
from Core.Data import globals

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
        self.selected_square = None
        self.board1_surf = self.create_board_surf()
        self.board2_surf = self.create_board_surf()
        self.standing_ships = self.num
        self.is_end = False
        if not globals.services[0].isPVP:
            globals.services[2].isPlayer1 = True


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
            if globals.services[2].isPlayer1:
                ship, x, y = self.get_square_under_mouse(self.board.shotBoard1)
            else:
                ship, x, y = self.get_square_under_mouse(self.board.shotBoard2)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.MOUSEBUTTONUP:
                    if ship == 0:
                        self.selected_square = ship, x, y

                    
            globals.surface[0].fill((228, 230, 246))
            globals.surface[0].blit(self.board1_surf, self.board1pos)
            globals.surface[0].blit(self.board2_surf, self.board2pos)

            s = self.titleFont.render("Destroy the enemy", True, pygame.Color("black"))
            s2 = self.titleFont.render("Destroy the enemy", True, pygame.Color("darkgrey"))
            globals.surface[0].blit(s2, (1, 1))
            globals.surface[0].blit(s, (0, 0))
            
            self.draw_selector(globals.surface[0], ship, x, y)
            if globals.services[2].isPlayer1:
                self.draw_ships(self.board.board1)
                self.draw_hits()
            else:
                self.draw_ships(self.board.board2)
                self.draw_hits()

            self.fire_button = Button(globals.surface[0], self.resx - 100, self.resy - 50, 100, 50, text = "FIRE", onClick = self.fire)
            self.reset_shots = Button(globals.surface[0], 0, self.resy - 50, 100, 50, text = "reset shots", onClick = self.reset_shot)
            self.pause_button = Button(globals.surface[0], self.resx - 50, 0, 50, 50, text = "||", onClick = self.build_pause_screen)

            if self.is_end:
                self.build_endgame_screen()
            
            pygame_widgets.update(events)
            pygame.display.update()

            pygame.display.flip()
            self.clock.tick(30)
            self.selected_square = None

    def draw_ships(self, board):
        if globals.services[2].isPlayer1:
            s = self.titleFont.render("Player 1 " + globals.account1[0].user, True, pygame.Color("black"))
        else:
            s = self.titleFont.render("Player 2 " + globals.account2[0].user, True, pygame.Color("black"))
        globals.surface[0].blit(s, (self.resx / 2 - 100, self.resy / 2 - self.tile_size * (self.num / 2) - 50))
        for x in range(self.num):
            for y in range(self.num):
                if board[y][x] != 0:
                    s1 = self.font.render("s" + str(board[y][x] + 1), True, pygame.Color("black"))
                    s2 = self.font.render("s" + str(board[y][x] + 1), True, pygame.Color("darkgrey"))
                    pos = pygame.Rect(self.board1pos[0] + x * self.tile_size+1, self.board1pos[1] + y * self.tile_size + 1, self.tile_size, self.tile_size)
                    globals.surface[0].blit(s2, s2.get_rect(center = pos.center).move(1, 1))
                    globals.surface[0].blit(s1, s1.get_rect(center = pos.center))

    def draw_hits(self):
        if self.selected_square:
            if globals.services[2].isPlayer1:
                self.board.shotBoard1[self.selected_square[2]][self.selected_square[1]] = 0
            else:
                self.board.shotBoard2[self.selected_square[2]][self.selected_square[1]] = 0

        for x in range(self.num):
            for y in range(self.num):
                if self.board.shotBoard1[y][x] == 1 and globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] == 1 and globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] == 1 and not globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard1[y][x] == 1 and not globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (0, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard1[y][x] == 2 and globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] == 2 and globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] == 2 and not globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard1[y][x] == 2 and not globals.services[2].isPlayer1:
                    center = [x * self.tile_size + self.board1pos[0] + (self.tile_size / 2), y * self.tile_size + self.board1pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], (255, 0, 0), center, self.tile_size / 2 - 5)
                if self.board.shotBoard1[y][x] == 0:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], pygame.color.Color("grey"), center, self.tile_size / 2 - 5)
                if self.board.shotBoard2[y][x] == 0:
                    center = [x * self.tile_size + self.board2pos[0] + (self.tile_size / 2), y * self.tile_size + self.board2pos[1] + (self.tile_size / 2)]
                    pygame.draw.circle(globals.surface[0], pygame.color.Color("grey"), center, self.tile_size / 2 - 5)
    
    def fire(self):
        shots = []
        startP1 = globals.services[2].isPlayer1
        hit = False
        if startP1:
            board = self.board.shotBoard1
            shipBoard = self.board.board2
            shipRemainingBoard = self.board.board1
        else:
            board = self.board.shotBoard2
            shipBoard = self.board.board1
            shipRemainingBoard = self.board.board2
        self.standing_ships = globals.services[2].get_standing_ships(shipRemainingBoard)
        for x in range(self.num):
            for y in range(self.num):
                if board[y][x] == -1:
                    shots.append([y, x])
        if self.board.salvo and len(shots) != len(self.standing_ships):
            messagebox.showerror("Invalid number of shots", "The number of shots you attempted to fire is invalid given your chosen settings, please try again")
            self.run_screen()
        if not self.board.salvo and len(shots) != 1:
            messagebox.showerror("Invalid number of shots", "The number of shots you attempted to fire is invalid given your chosen settings, please try again")
            self.run_screen()
        if self.board.chain:
            self.standing_ships, self.is_end = globals.services[2].chain_fire(shots, board, shipBoard)
        elif not self.board.chain and globals.services[0].isPVP:
            self.standing_ships, self.is_end = globals.services[2].fire(shots, board, shipBoard)
        if startP1 != globals.services[2].isPlayer1 and not self.is_end and globals.services[0].isPVP:
            tScreen = TransitionScreen()
            tScreen.run_screen()
        elif not globals.services[0].isPVP:
            self.standing_ships, self.is_end = globals.services[2].fire(shots, board, shipBoard)
            self.board.shotBoard2, self.board.board1, hit, self.is_end = globals.services[3].fire(self.board.board1, self.board.board2, self.board.shotBoard2, self.num, self.board.salvo)
            while hit and self.board.chain:
                self.board.shotBoard2, self.board.board1, hit, self.is_end = globals.services[3].fire(self.board.board1, self.board.board2, self.board.shotBoard2, self.num, self.board.salvo)
            globals.services[2].isPlayer1 = not globals.services[2].isPlayer1

    def reset_shot(self):
        if globals.services[2].isPlayer1:
            board = self.board.shotBoard1
        else:
            board = self.board.shotBoard2
        for x in range(self.num):
            for y in range(self.num):
                if board[x][y] == -1:
                    board[x][y] = 0
    
    def build_pause_screen(self):
        self.pause_screen = PauseScreen(self.board)
        self.pause_screen.add_elements()
    
    def build_endgame_screen(self):
        if globals.services[2].isPlayer1:
            globals.services[0].recordWin(globals.account2[0].key)
            globals.services[0].recordLoss(globals.account1[0].key)
        else:
            globals.services[0].recordWin(globals.account1[0].key)
            globals.services[0].recordLoss(globals.account2[0].key)

        self.endgame_screen = EndgameScreen()
        self.endgame_screen.add_elements()