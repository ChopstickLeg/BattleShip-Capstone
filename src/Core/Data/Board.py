class Board(object):
    def __init__(self, size, ship5, ship4, ship3, ship2, salvo, chain, board1 = None, board2 = None, shotBoard1 = None, shotBoard2 = None):
        self.size = size
        self.ship5 = ship5
        self.ship4 = ship4
        self.ship3 = ship3
        self.ship2 = ship2
        self.salvo = salvo
        self.chain = chain
        if not board1:
            self.board1 = [[0 for i in range(size)]for i in range(size)]
            self.board2 = [[0 for i in range(size)]for i in range(size)]
            self.shotBoard1 = [[0 for i in range(size)] for i in range(size)]
            self.shotBoard2 = [[0 for i in range(size)] for i in range(size)]
        else:
            self.board1 = board1
            self.board2 = board2
            self.shotBoard1 = shotBoard1
            self.shotBoard2 = shotBoard2
        self.ship_list = []
        for x in range(ship5):
            self.ship_list.append(5)
        for x in range(ship4):
            self.ship_list.append(4)
        for x in range(ship3):
            self.ship_list.append(3)
        for x in range(ship2):
            self.ship_list.append(2)