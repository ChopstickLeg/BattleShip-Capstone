from .BoardManagementServiceInterface import BoardManagementServiceInterface as BMSI
from ..Data.Board import Board
from Core.Data import globals
class BoardManagementService(BMSI):
    def __init__(self):
        self.board = None
    
    def generate_board(self, size, ship5, ship4, ship3, ship2, player1, player2 = None, salvo = False, chain = False):
        globals.rules.append([size, ship5, ship4, ship3, ship2, player1, player2, salvo, chain])
        self.board = Board(size, ship5, ship4, ship3, ship2, player1, player2, salvo, chain)
        return self.board
    
    def verify_placement(self, board, x, y, lastPlaced, currentLength, length, num):
        diff = []
        if currentLength >= length:
            return False
        if currentLength == 0:
            return True
        else:
            diff = [x - lastPlaced[0], y - lastPlaced[1]]
            if diff[0] > 0 or diff[0] < 0:
                for i in range(currentLength + 1):
                    if board[x+(i * diff[0] * -1)][y] != num and i != 0:
                        return False
            else:
                for i in range(currentLength):
                    if board[x][y + (i * diff[1] * -1)] != num and i != 0:
                        return False
        return True