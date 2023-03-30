from abc import ABC, abstractmethod
from ..Data import *
class BoardManagementServiceInterface(object):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    
    @abstractmethod
    def generate_board(self, size, ship5, ship4, ship3, ship2, player1, player2, salvo, chain):
        raise NotImplementedError()