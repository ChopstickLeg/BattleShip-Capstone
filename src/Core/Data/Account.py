class Account():
    def __init__(self, user, passwd, gamesPlayed = 0, gamesWon = 0):
        self.key = None
        self.user = user
        self.passwd = passwd
        self.gamesPlayed = gamesPlayed
        self.gamesWon = gamesWon