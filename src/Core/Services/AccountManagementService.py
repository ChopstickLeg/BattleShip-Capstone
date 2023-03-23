from uuid import uuid4
from .AccountManagementServiceInterface import AccountManagementServiceInterface as AMSI
from ..Data.Account import Account
import sqlite3

class AccountManagementService(AMSI):
    def __init__(self):
        self.conn = sqlite3.connect(r".\BattleshipDB.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS Accounts (Key INTEGER PRIMARY KEY, Username VARCHAR(256) NOT NULL UNIQUE, Password VARCHAR(256) NOT NULL, GamesPlayed INTEGER NOT NULL, GamesWon INTEGER NOT NULL)""")

    def createAccount(self, user, passwd):
        newAccount = Account(user, passwd)
        self.c.execute("""INSERT INTO Accounts (Username, Password, GamesPlayed, GamesWon) VALUES (?, ?, ?, ?)""", (user, passwd, 0, 0))
        self.conn.commit()
        return newAccount
    
    def getAccount(self, id):
        self.c.execute("""SELECT Username FROM Accounts WHERE Key = ?""", (id, ))
        user = self.c.fetchall()
        self.c.execute("""SELECT Password FROM Accounts WHERE Key = ?""", (id, ))
        passwd = self.c.fetchall()
        self.c.execute("""SELECT GamesPlayed FROM Accounts WHERE Key = ?""", (id, ))
        gamesPlayed = self.c.fetchall()
        self.c.execute("""SELECT GamesWon FROM Accounts WHERE Key = ?""", (id, ))
        gamesWon = self.c.fetchall()
        return Account(user, passwd, gamesPlayed, gamesWon)
    
    def loginAccount(self, user, passwd):
        self.c.execute("""SELECT Key FROM Accounts WHERE Username = ? AND Password = ?""", (user, passwd))
        out = self.c.fetchall()
        return self.getAccount(out[0][0])

    def recordWin(self, id):
        acct = self.getaccount(id)
        self.c.execute("""UPDATE Accounts SET GamesPlayed = ?, GamesWon = ? WHERE Key = ?""", (acct.gamesPlayed + 1, acct.gamesWon + 1, id))

    def recordLoss(self, id):
        acct = self.getaccount(id)
        self.c.execute("""UPDATE Accounts SET GamesPlayed = ? WHERE Key = ?""", (acct.gamesPlayed + 1, id))