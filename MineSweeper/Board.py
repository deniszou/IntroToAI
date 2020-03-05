import numpy
import os
class Board:
    def __init__(self, dim, numMines):
        self.dim = dim
        self.numMines = numMines
        # create an array with number of mines
        self.board = numpy.zeros((dim * dim))
        i = 0
        while numMines > 0:
            board[i] = 'm'
            i -= 1
        # shuffle the array
        numpy.random.shuffle(board)
        board.reshape((dim, dim))
        # iterate through the array and number non-mine pieces based on search or surrounding mines
        for x in range(dim):
            for y in range(dim):
                if board[(x, y)] == 'm':
                    continue
                else:
                    board[(x, y)] = checkMines(board, x, y)


    def checkMines(self, x, y):
        mineCount = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and y == 0:
                    continue
                if isValid(self, x + i, y + j):
                    if self.board[x + i, y + j] == 'm':
                        mineCount += 1
        self.board[x, y] == mineCount

    def isValid(self, x, y):
        if x < 0 or y < 0 or (x > self.dim - 1) or y > (self.dim - 1):
            return False
        return True
