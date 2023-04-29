from .UI_Interface import UI_Interface as UII
from Core.Data import globals
import pygame
import pygame_menu
import pygame_menu.locals

class LeaderboardScreen(UII):
    def add_elements(self):
        self.return_flag = False
        self.leaderboard = pygame_menu.Menu("Leaderboard", globals.resx[0], globals.resy[0], theme = pygame_menu.themes.THEME_BLUE)
        self.lb_table = self.leaderboard.add.table()
        self.lb_table.add_row(["\tRank\t", "\tUsername\t", "\tGames Won\t", "\tGames Played\t"])
        self.leaderboard.add.button("Return", self.swap_flag)
        self.leaderboard.enable()
        self.add_lb_items()
        self.lb_table.update_cell_style(-1, -1, align = "align-center", border_color = "black")
        self.run_screen(self.leaderboard)
    
    def swap_flag(self):
        self.return_flag = True

    def add_lb_items(self):
        table = globals.services[0].getAccounts()
        tb_out = []
        for item in table:
            tb_out.append([item.user, item.gamesWon, item.gamesPlayed])
        tb_out = sorted(tb_out, key=lambda wins: tb_out[1])
        for i in range(len(tb_out)):
            self.lb_table.add_row([str(i), str(tb_out[i][0]), str(tb_out[i][1]), str(tb_out[i][2])])
    
    def run_screen(self, menu):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            menu.update(events)
            menu.draw(globals.surface[0])
            pygame.display.flip()
            if self.return_flag:
                return