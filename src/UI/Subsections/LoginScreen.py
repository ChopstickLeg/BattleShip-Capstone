from .UI_Interface import *
from .CreateAccountScreen import CreateAccountScreen
import pygame
import pygame_menu
from tkinter import messagebox

class LoginScreen(UI_Interface):
    def __init__(self, service):
        self.accountService = service
        self.login_screen = pygame_menu.Menu("Login",100, 200, theme=pygame_menu.themes.THEME_BLUE)
        self.add_elements()
    
    def add_elements(self):
        self.login_user_input = self.login_screen.add.text_input("Username: ")
        self.login_pass_input = self.login_screen.add.text_input("Password: ")
        self.login_screen.add.button("Create Account", CreateAccountScreen.__init__)
        self.login_screen.add.button("Login", self.login_pressed)
        self.login_screen.add.button("Exit", pygame_menu.events.EXIT)
        self.on_resize(self.login_screen)
        self.login_screen.enable()
        super.run_screen(self.login_screen)
    
    def login_pressed(self):
        self.logged_in1, self.logged_in2 = self.accountService.get_logged_in()
        if self.logged_in1 == None:
            try:
                self.logged_in1 = self.accountService.loginAccount(self.login_user_input.get_value(), self.login_pass_input.get_value())
            except IndexError:
                messagebox.showerror(title="Account not found", message="An account with that user information could not be found, please try again")
                self.run_screen(self.loginScreen)
            self.create_mode_selection_screen()
        elif self.logged_in2 == None:
            try:
                if self.login_user_input.get_value() == self.logged_in1.user[0][0]:
                    messagebox.showerror(title="Same user login", message="The same user cannot be logged in twice.")
                    self.login_pass_input.clear()
                    self.login_user_input.clear()
                    self.run_screen(self.loginScreen)
                self.logged_in2 = self.accountService.loginAccount(self.login_user_input.get_value(), self.login_pass_input.get_value())
            except IndexError:
                messagebox.showerror(title="Account not found", message="An account with that user information could not be found, please try again")
                self.run_screen(self.loginScreen)
            self.create_rule_selection_screen()
        else:
            messagebox.showerror(title= "An error has occurred", message= "I don't know how you tried to login 3 accounts, but good job. Application will exit now")
            pygame_menu.events.EXIT
