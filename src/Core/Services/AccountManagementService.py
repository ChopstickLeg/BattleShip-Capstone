from uuid import uuid4
from .AccountManagementServiceInterface import AccountManagementServiceInterface as AMSI
from ..Data import Account
import sqlite3

class AccountManagementService(AMSI):
    def __init__(self):
        self.conn = sqlite3.connect(r".\BattleshipDB.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS Accounts (Key INTEGER PRIMARY KEY, Name VARCHAR(256) NOT NULL, Password VARCHAR(256) NOT NULL, GamesPlayed INTEGER NOT NULL, GamesWon INTEGER NOT NULL)""")

    def createAccount(self, user, passwd):
        newAccount = Account(user, passwd)
        self.c.execute("""INSERT INTO Accounts (Name, Password, GamesPlayed, GamesWon) VALUES (?, ?, ?, ?)""", (user, passwd, 0, 0))
    
    def getaccount(self, id, conn):
        return super().getaccount(id, conn)
    def loginAccount(self, user, passwd, conn):
        return super().loginAccount(user, passwd, conn)
    def recordWin(self, id, conn):
        return super().recordWin(id, conn)
    def recordLoss(self, id, conn):
        return super().recordLoss(id, conn)