import random
from .GameplayServiceInterface import GameplayServiceInterface as GMSI
class GamePlayService(GMSI):
    def __init__(self):
        if random.randint(0, 1) == 0:
            self.isPlayer1 = True
        else:
            self.isPlayer1 = False
    
    def fire(self, shots, board):
        self.isPlayer1 = not self.isPlayer1
        for item in shots:
            board[item[0]][item[1]] = 1
        return board