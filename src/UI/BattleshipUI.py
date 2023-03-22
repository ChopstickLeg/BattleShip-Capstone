import pygame
import pygame_menu
from Core.Services import AccountManagementServiceInterface
from Core.Services.AccountManagementService import AccountManagementService
from tkinter import messagebox

class BattleshipUI(object):
    def __init__(self) -> None:
        pygame.init()
        self.serviceCollection = {AccountManagementServiceInterface: AccountManagementService()}
        self.surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.accountService:AccountManagementServiceInterface = self.serviceCollection[AccountManagementServiceInterface]

    def create_login_screen(self):
        self.loginScreen = pygame_menu.Menu("Login",100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.login_user_input = self.loginScreen.add.text_input("Username: ")
        self.login_pass_input = self.loginScreen.add.text_input("Password: ")
        self.loginScreen.add.button("Create Account", self.create_create_account_screen)
        self.loginScreen.add.button("Login", self.login_pressed)
        self.loginScreen.add.button("Exit", pygame_menu.events.EXIT)
        self.on_resize(self.loginScreen)
        self.loginScreen.enable()
        self.run_screen(self.loginScreen)

    def create_create_account_screen(self):
        self.create_account_screen = pygame_menu.Menu("Create Account", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.create_user_input = self.create_account_screen.add.text_input("Username: ")
        self.create_pass_input = self.create_account_screen.add.text_input("Password: ")
        self.create_pass_confirm_input = self.create_account_screen.add.text_input("Confirm Password: ")
        self.create_account_screen.add.button("Create Account", self.create_account_pressed)
        self.create_account_screen.add.button("Exit", pygame_menu.events.EXIT)
        self.on_resize(self.create_account_screen)
        self.create_account_screen.enable()
        self.run_screen(self.create_account_screen)

    def create_mode_selection_screen(self):
        self.mode_selection_screen = pygame_menu.Menu("Select A Mode", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.mode_selection_screen.add.button("Player v Player", self.create_rule_selection_screen)
        self.mode_selection_screen.add.button("Player v Computer", self.create_rule_selection_screen)
        self.mode_selection_screen.add.button("Resume Game", self.create_saved_games_screen)
        self.mode_selection_screen.add.button("Quit Application", pygame_menu.events.EXIT)
        self.on_resize(self.mode_selection_screen)
        self.mode_selection_screen.enable()
        self.run_screen(self.mode_selection_screen)
    
    def create_saved_games_screen(self):
        self.saved_games_screen = pygame_menu.Menu("Select a saved game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.saved_games_screen.add.button("Saved game from <time> with players <player1> <player2>")
        self.saved_games_screen.add.button("Next screen", self.create_rule_selection_screen)
        self.on_resize(self.saved_games_screen)
        self.saved_games_screen.enable()
        self.run_screen(self.saved_games_screen)
    
    def create_rule_selection_screen(self):
        self.rule_selection_screen = pygame_menu.Menu("Select Your Rules", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.rule_selection_screen.add.dropselect(title = "Select Board Size", items = ["7 x 7", "8 x 8", "9 x 9", "10 x 10", "11 x 11", "12 x 12", "13 x 13"])
        self.rule_selection_screen.add.dropselect(title = "Select number of 5 length ships", items = ["1", "2", "3"])
        self.rule_selection_screen.add.dropselect(title = "Select number of 4 length ships", items = ["1", "2", "3", "4"])
        self.rule_selection_screen.add.dropselect(title = "Select number of 3 length ships", items = ["1", "2", "3", "4", "5"])
        self.rule_selection_screen.add.dropselect(title = "Select numebr of 2 length ships", items = ["1", "2", "3", "4", "5", "6"])
        self.rule_selection_screen.add.toggle_switch(title="Salvo Mode")
        self.rule_selection_screen.add.toggle_switch(title="Chain hits")
        self.rule_selection_screen.add.button("Next Screen", self.create_ship_placement_screen)
        self.rule_selection_screen.add.button("Exit Application", pygame_menu.events.EXIT)
        self.on_resize(self.rule_selection_screen)
        self.rule_selection_screen.enable()
        self.run_screen(self.rule_selection_screen)
    
    def create_ship_placement_screen(self):
        self.ship_placement_screen = pygame_menu.Menu("Place your ships", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.table1 = self.ship_placement_screen.add.table(border_color = "black")
        for n in range(10):
            self.table1.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
        self.ship_placement_screen.add.button("Next Screen", self.create_gameplay_screen)
        self.on_resize(self.ship_placement_screen)
        self.ship_placement_screen.enable()
        self.run_screen(self.ship_placement_screen)
    
    def create_gameplay_screen(self):
        self.gameplay_screen = pygame_menu.Menu("Play the game", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.table2 = self.gameplay_screen.add.table(border_color = "black")
        self.table3 = self.gameplay_screen.add.table(border_color = "black")
        for n in range(10):
            self.table2.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
            self.table3.add_row(["\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t"])
        self.gameplay_screen.add.button("Next Screen", self.create_pause_screen)
        self.on_resize(self.gameplay_screen)
        self.gameplay_screen.enable()
        self.run_screen(self.gameplay_screen)

    def create_pause_screen(self):
        self.pause_screen = pygame_menu.Menu("Game Paused", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.pause_screen.add.button("Resume game")
        self.pause_screen.add.button("Save & quit")
        self.pause_screen.add.button("Next Screen", self.create_endgame_screen)
        self.pause_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.pause_screen)
        self.pause_screen.enable()
        self.run_screen(self.pause_screen)

    def create_endgame_screen(self):
        self.endgame_screen = pygame_menu.Menu("Game Over", 100, 200, theme = pygame_menu.themes.THEME_BLUE)
        self.endgame_screen.add.button("Rematch")
        self.endgame_screen.add.button("Return to login")
        self.endgame_screen.add.button("Quit application", pygame_menu.events.EXIT)
        self.on_resize(self.endgame_screen)
        self.endgame_screen.enable()
        self.run_screen(self.endgame_screen)

    def login_pressed(self):
        self.logged_in1 = self.accountService.loginAccount(self.login_user_input.get_value(), self.login_pass_input.get_value())
        self.create_mode_selection_screen()

    def create_account_pressed(self):
        if self.create_pass_confirm_input.get_value() != self.create_pass_input.get_value():
            self.create_pass_input.clear()
            self.create_pass_confirm_input.clear()
            messagebox.showerror(title = "Password Error", message = "Passwords do not match")
            self.run_screen()
        self.accountService.createAccount(self.create_user_input.get_value(), self.create_pass_input.get_value())
        self.create_login_screen()

    def run_screen(self, menu):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.VIDEORESIZE:
                    self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.on_resize(menu)
            menu.update(events)
            menu.draw(self.surface)
            pygame.display.flip()
    
    def on_resize(self, menu):
        windowSize = self.surface.get_size()
        newW, newH = windowSize[0], windowSize[1]
        menu.resize(newW, newH)