import random
from ComputerManagementServiceInterface import ComputerManagementServiceInterface as CMSI
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
        recurse = False
        for i in range(len(ships)):
            start = (random.randint(0, size - 1), random.randint(size - 1))
            while board[start[0]][start[1]] != -1:
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
            while count < ships[i]:
                if len(attempted) == 4:
                    for x in range(size):
                        for y in range(size):
                            if board[x][y] != -1:
                                board[x][y] = -1
                    recurse = True
                    break
                count += 1
                if board[current[0] + cords[0]][current[1] + cords[1]] == -1:
                    current = tuple(map(lambda x, y: x+y, current, cords))
                    board[current[0]][current[1]] = i + 1
                else:
                    attempted.append(direction)
                    for n in range(count):
                        board[current[0] + -1 * (cords[0] * n)][current[1] + -1 * (cords[1] * n)] = -1
                    while direction not in attempted and len(attempted) != 4:
                        direction = random.randint(1, 4)
                    count = 0
            if recurse:
                break
        if recurse:
            self.place_ships(size, ships, board)
        else:
            return board
    
    def fire(self, shipBoard, shotBoard, size):
        hit = False
        place = (random.randint(0, size), random.randint(0, size))
        while shotBoard[place[0]][place[1]] != -1:
            place = (random.randint(0, size), random.randint(0, size))
        if shipBoard[place[0]][place[1]] == -1:
            shotBoard[place[0]][place[1]] = 1
        else:
            shotBoard[place[0]][place[1]] = 2
            shipBoard[place[0]][place[1]] = -1
            hit = True
        return shotBoard, shipBoard, hit
    
    def fire_salvo()
        