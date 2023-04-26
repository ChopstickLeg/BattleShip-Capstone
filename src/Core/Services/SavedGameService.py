import os
from Core.Data import globals
from Core.Data.Board import Board
import time
class SavedGameService(object):
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "Saved_Games")
        try:
            self.file_list = os.listdir(self.path)
        except FileNotFoundError:
            self.file_list = []
        self.bs_games = []
        for item in self.file_list:
            if item[:-4] == ".txt":
                self.bs_games.append(item)
    
    def get_saved_games(self):
        self.games = []
        for i in range(len(self.bs_games)):
            info = self.bs_games[i].split("-")
            self.games.append(i, info)
        return self.games
    
    def save_game(self, board):
        current_time = time.localtime()
        file_name = globals.account1[0].user + "-" + globals.account2[0].user + "-" + str(current_time[0]) + "-" +  str(current_time[1]) + "-" + str(current_time[2]) + "-" + str(current_time[3]) + "-" + str(current_time[4])
        out_path = str(os.path.join(self.path, file_name + ".txt"))
        with open(out_path, "x") as out:
            out.write(str(board.size) + "\n" + str(board.ship_list) + "\n" + str(board.salvo)
                      + "\n" + str(board.chain) + '\n')
            for item in board.board1:
                out.write(str(item) + ".")
            for item in board.board2:
                out.write(str(item) + ".")
            for item in board.shotBoard1:
                out.write(str(item) + ".")
            for item in board.shotBoard2:
                out.write(str(item) + ".")
    
    def load_saved_game(self, file_info):
        size = 0
        ship_list = []
        salvo = None
        chain = None
        board1 = []
        board2 = []
        shotBoard1 = []
        shotBoard2 = []
        temp = []
        fName = ""
        for item in file_info:
            fName += item + "-"
        fName = fName[:-1] + ".txt"
        with open(fName, "r") as f:
            size = int(f.readline().strip())
            for char in f.readline().split(","):
                if char.isdigit():
                    ship_list.append(int(char))
            salvo = bool(f.readline().strip())
            chain = bool(f.readline().strip())
            for char in f.readline().split("."):
                for data in char.split(","):
                    if data.isdigit():
                        temp.append(data)
                board1.append(temp)
                temp = []
            for char in f.readline().split("."):
                for data in char.split(","):
                    if data.isdigit():
                        temp.append(data)
                board2.append(temp)
                temp = []
            for char in f.readline().split("."):
                for data in char.split(","):
                    if data.isdigit():
                        temp.append(data)
                shotBoard1.append(temp)
                temp = []
            for char in f.readline().split("."):
                for data in char.split(","):
                    if data.isdigit():
                        temp.append(data)
                shotBoard2.append(temp)
                temp = []
        return size, ship_list, salvo, chain, board1, board2, shotBoard1, shotBoard2