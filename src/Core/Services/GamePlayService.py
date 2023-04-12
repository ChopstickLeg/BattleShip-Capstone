import random
from .GameplayServiceInterface import GameplayServiceInterface as GMSI
class GamePlayService(GMSI):
    def __init__(self):
        if random.randint(0, 1) == 0:
            self.isPlayer1 = True
        else:
            self.isPlayer1 = False
        #This is just here for testing purposes, and will be removed later
        self.isPlayer1 = True
    
    def fire(self, shots, shotBoard, shipBoard):
        self.isPlayer1 = not self.isPlayer1
        for item in shots:
            if shipBoard[item[0]][item[1]] != -1:
                shipBoard[item[0]][item[1]] = -1
                shotBoard[item[0]][item[1]] = 2
            else:
                shotBoard[item[0]][item[1]] = 1
        return shotBoard, shipBoard
    
    def chain_fire(self, shots, shotBoard, shipBoard):
        hasHit = False
        for item in shots:
            if shipBoard[item[0]][item[1]] != -1:
                shipBoard[item[0]][item[1]] = -1
                shotBoard[item[0]][item[1]] = 2
                if not hasHit:
                    hasHit = True
                    self.isPlayer1 = not self.isPlayer1
            else:
                shotBoard[item[0]][item[1]] = 1
        return shotBoard, shipBoard