class Board(object):
    def __init__(self, size, ship5, ship4, ship3, ship2, player1, player2, salvo =False, chain = False):
        self.size = size
        self.ship5 = ship5
        self.ship4 = ship4
        self.ship3 = ship3
        self.ship2 = ship2
        self.player1 = player1
        self.player2 = player2
        self.salvo = salvo
        self.chain = chain
        self.board1 = [[0 for i in range(size)]for i in range(size)]
        self.board2 = [[0 for i in range(size)]for i in range(size)]
        self.shotBoard1 = [[0 for i in range(size)] for i in range(size)]
        self.shotBoard2 = [[0 for i in range(size)] for i in range(size)]
        self.ship_list = []
        for x in range(ship5):
            self.ship_list.append(5)
        for x in range(ship4):
            self.ship_list.append(4)
        for x in range(ship3):
            self.ship_list.append(3)
        for x in range(ship2):
            self.ship_list.append(2)