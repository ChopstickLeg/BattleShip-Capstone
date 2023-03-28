from .UI_Interface import *
import pygame
import pygame_menu
from tkinter import messagebox

class CreateAccountScreen(UI_Interface):
    def __init__(self):
        self.create_account_screen = pygame_menu.Menu("Create Account", 100, 200, theme=pygame_menu.themes.THEME_BLUE)