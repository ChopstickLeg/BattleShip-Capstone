import pygame
from .Subsections.AccountScreens import AccountsScreens
from Core.Services import AccountManagementServiceInterface
from Core.Services.AccountManagementService import AccountManagementService
from Core.Services.BoardManagementService import BoardManagementService
from Core.Services import BoardManagementServiceInterface
from Core.Data import globals

class BattleshipUI(object):
    def __init__(self) -> None:
        pygame.init()
        globals.init()
        #Maybe set these all as global variables at some point
        self.serviceCollection = {AccountManagementServiceInterface: AccountManagementService(), BoardManagementServiceInterface: BoardManagementService()}
        self.surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.accountService:AccountManagementServiceInterface = self.serviceCollection[AccountManagementServiceInterface]
        self.boardService:BoardManagementServiceInterface = self.serviceCollection[BoardManagementServiceInterface]
        self.login_screen = AccountsScreens(self.accountService, self.boardService, self.surface)
        self.login_screen.add_login_elements()
    
    