import random
from .GameplayServiceInterface import GameplayServiceInterface as GMSI
class GamePlayService(GMSI):
    def __init__(self):
        if random.randint(0, 1) == 0:
            self.isPlayer1 = True
        else:
            self.isPlayer1 = False
    
    def fire(self, shots, shotBoard, shipBoard):
        hit = False
        end = False
        self.isPlayer1 = not self.isPlayer1
        for item in shots:
            if shipBoard[item[0]][item[1]] != 0:
                shipBoard[item[0]][item[1]] = 0
                shotBoard[item[0]][item[1]] = 2
                hit = True
            else:
                shotBoard[item[0]][item[1]] = 1
        ship_standing = self.get_standing_ships(shipBoard)
        if len(ship_standing) == 0:
            end = True
        return ship_standing, end, hit
    
    def get_standing_ships(self, shipBoard):
        ship_standing = set()
        for x in range(len(shipBoard)):
            for y in range(len(shipBoard)):
                if shipBoard[y][x] != 0:
                    ship_standing.add(shipBoard[y][x])
        return ship_standing