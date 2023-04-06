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
        infoObject = pygame.display.Info()
        globals.surface.append(pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN))
        globals.services.append(self.serviceCollection[AccountManagementServiceInterface])
        globals.services.append(self.serviceCollection[BoardManagementServiceInterface])
        self.login_screen = AccountsScreens()
        self.login_screen.add_login_elements()
    
    