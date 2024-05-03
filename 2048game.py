import os
import sys
import random
clear = lambda: os.system("cls")

class Game2048:
    """The default 4x4 2048 game made in python.
    
    Attributes
    ----------
    board : list
        The game board represented as list
    columns : list
        The indexed of board columns
    """
    
    def __init__(self):
        self.board = [0 for i in range(16)]
        self.__initColumns()
        self.__insertRandom()
        self.__insertRandom()
    
    def __initColumns(self):
        self.columns = []
        for i in range(4):
            column = []
            for j in range(i, len(self.board), 4):
                column.append(j)
            self.columns.append(column)
    
    def __insertRandom(self):
        """Insert new numbers on empty fiels randomly."""
        emptys = []
        for i in range(len(self.board)):
            if self.board[i] == 0: emptys.append(i)
        if len(emptys) == 0: return
        index = random.choice(emptys)
        self.board[index] = random.choice([2,2,2,2,2,2,2,2,2,4])
    
    def printBoard(self, colored=False):
        """Prints the current game board.
        
        Parameters
        ----------
        colored : bool, optional
            The numbers are displayed in color
        """
        for i in range(0, len(self.board), 4):
            row = self.board[i:i+4]
            if not colored: print("\t|\t".join(str(n).replace("0", " ") for n in row))
            else: print("\t|\t".join(
                ("{" + str(n) + "}")
                    .replace("{0}", " ")
                    .replace("{2}", "\x1b[48;2;126;150;159m" + " 2 " + "\x1b[0m")
                    .replace("{4}", "\x1b[48;2;99;123;132m" + " 4 " + "\x1b[0m")
                    .replace("{8}", "\x1b[48;2;242;177;121m" + " 8 " + "\x1b[0m")
                    .replace("{16}", "\x1b[48;2;245;149;99m" + " 16 " + "\x1b[0m")
                    .replace("{32}", "\x1b[48;2;246;124;96m" + " 32 " + "\x1b[0m")
                    .replace("{64}", "\x1b[48;2;246;94;59m" + " 64 " + "\x1b[0m")
                    .replace("{128}", "\x1b[48;2;237;207;115m" + " 128 " + "\x1b[0m")
                    .replace("{256}", "\x1b[48;2;237;204;98m" + " 256 " + "\x1b[0m")
                    .replace("{512}", "\x1b[48;2;237;200;80m" + " 512 " + "\x1b[0m")
                    .replace("{1024}", "\x1b[48;2;237;197;63m" + " 1024 " + "\x1b[0m")
                    .replace("{2048}", "\x1b[48;2;237;194;45m" + " 2048 " + "\x1b[0m")
                for n in row))
            if i != 12: print("-" * 55)
            
    def merge(self, direction: str) -> bool:
        """Merges fields with the same value.
        
        Parameters
        ----------
        direction : str
            The direction in which should be merged
        
        Returns
        -------
        bool
            If something has merged
        """
        merged = False
        if direction == "left" or direction == "a":
            for i in range(0, len(self.board), 4):
                for j in range(1, 4):
                    if self.board[i+j] != 0 and self.board[i+j-1] == self.board[i+j]:
                        self.board[i+j-1] += self.board[i+j]
                        self.board[i+j] = 0
                        merged = True
        elif direction == "right" or direction == "d":
            for i in range(0, len(self.board), 4):
                for j in range(2, -1, -1):
                    if self.board[i+j] != 0 and self.board[i+j+1] == self.board[i+j]:
                        self.board[i+j+1] += self.board[i+j]
                        self.board[i+j] = 0
                        merged = True
        elif direction == "up" or direction == "w":
            for r in self.columns:
                for j in range(1, 4):
                    if self.board[r[j]] != 0 and self.board[r[j-1]] == self.board[r[j]]:
                        self.board[r[j-1]] += self.board[r[j]]
                        self.board[r[j]] = 0
                        merged = True
        elif direction == "down" or direction == "s":
            for r in self.columns:
                for j in range(2, -1, -1):
                    if self.board[r[j]] != 0 and self.board[r[j+1]] == self.board[r[j]]:
                        self.board[r[j+1]] += self.board[r[j]]
                        self.board[r[j]] = 0
                        merged = True
        return merged
    
    def shift(self, direction: str) -> bool:
        """Shift fields into a direction.
        
        Parameters
        ----------
        direction : str
            The direction in which should be shifted
        
        Returns
        -------
        bool
            If something has shifted
        """
        shifted = False
        if direction == "left" or direction == "a":
            for i in range(0, len(self.board), 4):
                for j in range(1, 4):
                    if self.board[i+j] != 0 and self.board[i+j-1] == 0:
                        self.board[i+j-1] = self.board[i+j]
                        self.board[i+j] = 0
                        shifted = True
        elif direction == "right" or direction == "d":
            for i in range(0, len(self.board), 4):
                for j in range(2, -1, -1):
                    if self.board[i+j] != 0 and self.board[i+j+1] == 0:
                        self.board[i+j+1] = self.board[i+j]
                        self.board[i+j] = 0
                        shifted = True
        elif direction == "up" or direction == "w":
            for r in self.columns:
                for j in range(1, 4):
                    if self.board[r[j]] != 0 and self.board[r[j-1]] == 0:
                        self.board[r[j-1]] = self.board[r[j]]
                        self.board[r[j]] = 0
                        shifted = True
        elif direction == "down" or direction == "s":
            for r in self.columns:
                for j in range(2, -1, -1):
                    if self.board[r[j]] != 0 and self.board[r[j+1]] == 0:
                        self.board[r[j+1]] = self.board[r[j]]
                        self.board[r[j]] = 0
                        shifted = True
        return shifted
    
    def move(self, direction: str):
        """Makes a game move.
        The main algorithms contains 2x shift, 1 merge and 1 shift.
        If the move is valid, insert a new number on an empty field randomly.
        
        Parameters
        ----------
        direction : str
            The direction in which should be moved
        """
        a = self.shift(direction)
        b = self.shift(direction)
        c = self.merge(direction)
        d = self.shift(direction)
        if a or b or c or d:
            self.__insertRandom()

if __name__ == "__main__":
    colored = False
    if len(sys.argv) == 2: colored = sys.argv[1] == "colored"
    clear()
    game = Game2048()
    while True:
        game.printBoard(colored)
        direction = input()
        if direction == "quit": break
        clear()
        game.move(direction)
