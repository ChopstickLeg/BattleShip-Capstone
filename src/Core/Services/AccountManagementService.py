from uuid import uuid4
from .AccountManagementServiceInterface import AccountManagementServiceInterface as AMSI
from ..Data.Account import Account
from Core.Data import globals
import sqlite3

class AccountManagementService(AMSI):
    def __init__(self):
        self.conn = sqlite3.connect(r".\BattleshipDB.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS Accounts (Key INTEGER PRIMARY KEY, Username VARCHAR(256) NOT NULL UNIQUE, Password VARCHAR(256) NOT NULL, GamesPlayed INTEGER NOT NULL, GamesWon INTEGER NOT NULL)""")
        self.c.execute("""INSERT INTO Accounts (Username, Password, GamesPlayed, GamesWon) SELECT 'Computer', 'None', 0, 0 WHERE NOT EXISTS (SELECT Username FROM Accounts WHERE Username = "Computer")""")
        self.conn.commit()
        self.logged_in1 = None
        self.logged_in2 = None
        self.isPVP = False

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
        returnAccount = Account(user[0][0], passwd[0][0], gamesPlayed[0][0], gamesWon[0][0], id)
        return returnAccount
    
    def loginAccount(self, user, passwd):
        self.c.execute("""SELECT Key FROM Accounts WHERE Username = ? AND Password = ?""", (user, passwd))
        out = self.c.fetchall()
        if self.logged_in1 == None:
            self.logged_in1 = self.getAccount(out[0][0])
            return self.logged_in1
        elif self.logged_in2 == None:
            self.logged_in2 = self.getAccount(out[0][0])
            return self.logged_in2
        
    
    def recordWin(self, id):
        acct = self.getAccount(id)
        self.c.execute("""UPDATE Accounts SET GamesPlayed = ?, GamesWon = ? WHERE Key = ?""", (acct.gamesPlayed + 1, acct.gamesWon + 1, id))
        globals.game_winner.append(self.getAccount(id))

    def recordLoss(self, id):
        acct = self.getAccount(id)
        self.c.execute("""UPDATE Accounts SET GamesPlayed = ? WHERE Key = ?""", (acct.gamesPlayed + 1, id))