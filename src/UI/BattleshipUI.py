import pygame
from .Subsections.AccountScreens import AccountsScreens
from Core.Services import AccountManagementServiceInterface
from Core.Services.AccountManagementService import AccountManagementService
from Core.Services.BoardManagementService import BoardManagementService
from Core.Services import BoardManagementServiceInterface
from Core.Services import GameplayServiceInterface
from Core.Services import ComputerManagementServiceInterface
from Core.Services.ComputerManagementService import ComputerManagementService
from Core.Services.GamePlayService import GamePlayService
from Core.Data import globals

class BattleshipUI(object):
    def __init__(self) -> None:
        pygame.init()
        globals.init()
        self.serviceCollection = {AccountManagementServiceInterface: AccountManagementService(), BoardManagementServiceInterface: BoardManagementService(), GameplayServiceInterface: GamePlayService(), ComputerManagementServiceInterface:ComputerManagementService()}
        infoObject = pygame.display.Info()
        globals.surface.append(pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN))
        size = globals.surface[0].get_size()
        globals.resx.append(size[0])
        globals.resy.append(size[1])
        globals.services.append(self.serviceCollection[AccountManagementServiceInterface])
        globals.services.append(self.serviceCollection[BoardManagementServiceInterface])
        globals.services.append(self.serviceCollection[GameplayServiceInterface])
        globals.services.append(self.serviceCollection[ComputerManagementServiceInterface])
        globals.services.append(self)
        self.login_screen = AccountsScreens()
        self.login_screen.add_login_elements()
    
    