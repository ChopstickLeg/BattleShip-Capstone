import pygame
import pygame_menu
from tkinter import messagebox
from .UI_Interface import UI_Interface as UII
from .RuleSelectionScreen import RuleSelectionScreen
from .SavedGameScreen import SavedGamesScreen
import sqlite3
from Core.Data import globals
from Core.Data import Account
class AccountsScreens(UII):
    def add_login_elements(self):
        self.login_screen = pygame_menu.Menu("Login",100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.login_user_input = self.login_screen.add.text_input("Username: ")
        self.login_pass_input = self.login_screen.add.text_input("Password: ")
        self.login_screen.add.button("Create Account", self.add_create_account_elements)
        self.login_screen.add.button("Login", self.login_pressed)
        self.login_screen.add.button("Exit", pygame_menu.events.EXIT)
        self.on_resize(self.login_screen)
        self.login_screen.enable()
        self.run_screen(self.login_screen)
    
    def add_create_account_elements(self):
        self.create_account_screen = pygame_menu.Menu("Create Account", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.create_user_input = self.create_account_screen.add.text_input("Username: ")
        self.create_pass_input = self.create_account_screen.add.text_input("Password: ")
        self.create_pass_confirm_input = self.create_account_screen.add.text_input("Confirm Password: ")
        self.create_account_screen.add.button("Create Account", self.create_account_pressed)
        self.create_account_screen.add.button("Back to Login", self.add_login_elements)
        self.create_account_screen.add.button("Exit", pygame_menu.events.EXIT)
        self.on_resize(self.create_account_screen)
        self.create_account_screen.enable()
        self.run_screen(self.create_account_screen)
    
    def add_mode_selection_elements(self):
        self.mode_selection_screen = pygame_menu.Menu("Select A Mode", 100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.logged_in1, self.logged_in2 = globals.services[0].get_logged_in()
        self.mode_selection_screen.add.label("Logged in as: " + globals.account1[0])
        self.mode_selection_screen.add.button("Player v Player", self.add_login_elements)
        self.mode_selection_screen.add.button("Player v Computer", self.build_rule_selection_screen)
        self.mode_selection_screen.add.button("Resume Game", self.build_saved_games_screen)
        self.mode_selection_screen.add.button("Quit Application", pygame_menu.events.EXIT)
        self.on_resize(self.mode_selection_screen)
        self.mode_selection_screen.enable()
        self.run_screen(self.mode_selection_screen)

    def build_rule_selection_screen(self):
        self.rule_selection_screen = RuleSelectionScreen()
        self.rule_selection_screen.add_elements()
    def build_saved_games_screen(self):
        self.saved_games_screen = SavedGamesScreen()
        self.saved_games_screen.add_elements()
    def login_pressed(self):
        self.logged_in1, self.logged_in2 = globals.services[0].get_logged_in()
        if self.logged_in1 == None:
            try:
                globals.account1.append(globals.services[0].loginAccount(self.login_user_input.get_value(), self.login_pass_input.get_value()))
            except IndexError:
                messagebox.showerror(title="Account not found", message="An account with that user information could not be found, please try again")
                self.run_screen(self.login_screen)
            self.add_mode_selection_elements()
        elif self.logged_in2 == None:
            try:
                if self.login_user_input.get_value() == self.logged_in1.user[0][0]:
                    messagebox.showerror(title="Same user login", message="The same user cannot be logged in twice.")
                    self.login_pass_input.clear()
                    self.login_user_input.clear()
                    self.run_screen(self.login_screen)
                globals.account2.append(globals.services[0].loginAccount(self.login_user_input.get_value(), self.login_pass_input.get_value()))
            except IndexError:
                messagebox.showerror(title="Account not found", message="An account with that user information could not be found, please try again")
                self.run_screen(self.login_screen)
            self.build_rule_selection_screen()
        else:
            messagebox.showerror(title= "An error has occurred", message= "I don't know how you tried to login 3 accounts, but good job. Application will exit now")
            pygame_menu.events.EXIT
    
    def create_account_pressed(self):
        if self.create_pass_confirm_input.get_value() != self.create_pass_input.get_value():
            self.create_pass_input.clear()
            self.create_pass_confirm_input.clear()
            messagebox.showerror(title = "Password Error", message = "Passwords do not match")
            self.run_screen(self.create_account_screen)
        try:
            globals.services[0].createAccount(self.create_user_input.get_value(), self.create_pass_input.get_value())
        except sqlite3.IntegrityError:
            messagebox.showerror(title="Duplicate Username", message="That username is already in use")
            self.create_user_input.clear()
            self.run_screen(self.create_account_screen)
        self.add_login_elements()