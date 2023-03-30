from .BoardManagementServiceInterface import BoardManagementServiceInterface as BMSI
from ..Data.Board import Board
class BoardManagementService(BMSI):
    def __init__(self):
        self.board = None
    
    def generate_board(self, size, ship5, ship4, ship3, ship2, player1, player2 = None, salvo = False, chain = False):
        self.board = Board(size, ship5, ship4, ship3, ship2, player1, player2, salvo, chain)
        return self.board