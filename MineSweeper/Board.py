import numpy
import os


class Board:
    def __init__(self, dim, numMines):
        self.dim = dim
        self.numMines = numMines

        # create an array with number of mines
        self.board = numpy.zeros((dim * dim), dtype=str)
        i = 0
        while numMines > 0:
            self.board[i] = 'm'
            i += 1
            numMines -= 1

        # shuffle the array
        numpy.random.shuffle(self.board)
        self.board = numpy.reshape(self.board, (dim, dim))

        # iterate through the array and number non-mine pieces based on search of surrounding mines
        for x in range(dim):
            for y in range(dim):
                if self.board[x, y] == 'm':
                    continue
                else:
                    Board.checkMines(self, x, y)

    def checkMines(self, x, y):
        mineCount = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if Board.isValid(self, x + i, y + j):
                    if self.board[x + i, y + j] == 'm':
                        mineCount += 1
        self.board[x, y] = mineCount

    def isValid(self, x, y):
        if x < 0 or y < 0 or (x > self.dim - 1) or y > (self.dim - 1):
            return False
        return True

    def printBoard(self):
        print(self.board)
