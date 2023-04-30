import random
from .ComputerManagementServiceInterface import ComputerManagementServiceInterface as CMSI
from .GamePlayService import GamePlayService as GPS
class ComputerManagementService(CMSI):
    def __init__(self):
        pass

    def place_ships(self, size, ships, board):
        start = ()
        current = ()
        count = 0
        direction = 0
        cords = []
        attempted = []
        recurse = True
        while recurse:
            for i in range(len(ships)):
                count = 0
                attempted = []
                recurse = False
                start = (random.randint(0, size - 1), random.randint(0, size - 1))
                while board[start[0]][start[1]] != 0:
                    start = (random.randint(0, size-1), random.randint(0, size - 1))
                current = start
                board[start[0]][start[1]] = i + 1
                direction = random.randint(1, 4)
                if direction == 1:
                    cords = (1, 0)
                elif direction == 2:
                    cords = (0, 1)
                elif direction == 3:
                    cords = (-1, 0)
                else:
                    cords = (0, -1)
                while count < ships[i] - 1:
                    if len(attempted) == 4:
                        for x in range(size):
                            for y in range(size):
                                if board[x][y] != 0:
                                    board[x][y] = 0
                        recurse = True
                        break
                    count += 1
                    if current[0] + cords[0] < size and current[1] + cords[1] < size and board[current[0] + cords[0]][current[1] + cords[1]] == 0 and current[0] + cords[0] > 0 and current[1] + cords[1] > 0:
                        current = tuple(map(lambda x, y: x+y, current, cords))
                        board[current[0]][current[1]] = i + 1
                    else:
                        attempted.append(direction)
                        for n in range(count - 1):
                            board[current[0] + -1 * (cords[0] * n)][current[1] + -1 * (cords[1] * n)] = 0
                        while direction in attempted and len(attempted) != 4:
                            direction = random.randint(1, 4)
                        if direction == 1:
                            cords = (1, 0)
                        elif direction == 2:
                            cords = (0, 1)
                        elif direction == 3:
                            cords = (-1, 0)
                        else:
                            cords = (0, -1)
                        count = 0
                        current = start
                if recurse:
                    break
        return board
    
    def fire(self, shipBoard, selfShips, shotBoard, size, salvo):
        hit = False
        end = False
        if salvo:
            shotNums = GPS.get_standing_ships(self, selfShips)
        else:
            shotNums = [1]
        place = (random.randint(0, len(shotBoard[0]) - 1), random.randint(0, len(shotBoard[0]) - 1))
        for i in range(len(shotNums)):
            while shotBoard[place[0]][place[1]] != 0:
                place = (random.randint(0, size - 1), random.randint(0, size - 1))
            if shipBoard[place[0]][place[1]] == 0:
                shotBoard[place[0]][place[1]] = 1
            else:
                shotBoard[place[0]][place[1]] = 2
                shipBoard[place[0]][place[1]] = 0
                hit = True
        if len(GPS.get_standing_ships(self, shipBoard)) == 0:
            end = True
        return shotBoard, shipBoard, hit, end