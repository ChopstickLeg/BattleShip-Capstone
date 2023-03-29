import pygame
from .Subsections.AccountScreens import AccountsScreens
from Core.Services import AccountManagementServiceInterface
from Core.Services.AccountManagementService import AccountManagementService

class BattleshipUI(object):
    def __init__(self) -> None:
        pygame.init()
        self.serviceCollection = {AccountManagementServiceInterface: AccountManagementService()}
        self.surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.accountService:AccountManagementServiceInterface = self.serviceCollection[AccountManagementServiceInterface]
        self.login_screen = AccountsScreens(self.accountService, self.surface)
        self.login_screen.add_login_elements()
    
    