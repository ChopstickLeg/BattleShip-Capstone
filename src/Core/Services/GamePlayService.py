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
        end = False
        self.isPlayer1 = not self.isPlayer1
        for item in shots:
            if shipBoard[item[0]][item[1]] != -1:
                shipBoard[item[0]][item[1]] = -1
                shotBoard[item[0]][item[1]] = 2
            else:
                shotBoard[item[0]][item[1]] = 1
        ship_standing = self.get_standing_ships(shipBoard)
        if len(ship_standing) == 0:
            end = True
        return ship_standing, end
    
    def chain_fire(self, shots, shotBoard, shipBoard):
        end = False
        hasHit = False
        for item in shots:
            if shipBoard[item[0]][item[1]] != -1:
                shipBoard[item[0]][item[1]] = -1
                shotBoard[item[0]][item[1]] = 2
                if not hasHit:
                    hasHit = True
            else:
                shotBoard[item[0]][item[1]] = 1
        if not hasHit:
            self.isPlayer1 = not self.isPlayer1
        ship_standing = self.get_standing_ships(shipBoard)
        if len(ship_standing) == 0:
            end = True
        return ship_standing, end
    
    def get_standing_ships(self, shipBoard):
        ship_standing = set()
        for x in range(len(shipBoard)):
            for y in range(len(shipBoard)):
                if shipBoard[y][x] != -1:
                    ship_standing.add(shipBoard[y][x])
        return ship_standing