from functools import reduce
import operator as op
from collections import Counter

import numpy


# This class will be used to play the game on Agent's own board
class ImprovedAgent:
    def __init__(self, board):
        self.gameOver = False
        self.gameBoard = board
        self.agentBoard = numpy.full((board.dim, board.dim), 'x')
        self.visitedSquares = []
        self.safeSquareStack = []
        self.possibleMineSquares = []
        self.explosions = 0

    def play(self):
        print("Playing Game...")
        turn = 1
        # self.gameBoard.printBoard()
        print("\n\n")

        # For the first turn we guess in the corner to optimize chances for solvability -coords (0,0)-
        self.clickSquare(0, 0)

        """" 
        Logic for improved agent loop:
        1) Check if safeSquareStack is populated. If it is, we pop the most recent off the stack
        and click on it. Else we iterate through our visitedSquares and try to gather new info
        by flagging mines and marking new safe spaces
        2) If we find new safeSquares from the visitedSquares, explore them. Otherwise, enumerate every
        possible board and choose square where a mine occurs the least.
        """

        while not self.gameOver:
            if self.safeSquareStack:  # If safeSquareStack is not empty, pop most recently added
                currentSquare = self.safeSquareStack.pop()
            else:
                for square in self.visitedSquares:  # Iterate through all visitedSquares to gather new info
                    surHidSquares = 0
                    surMines = 0
                    surSafeSquares = 0
                    # print("SQUARE: ", square)
                    clue = self.gameBoard.board[square]
                    x = square[0]
                    y = square[1]
                    if clue.isdigit():
                        # Check surrounding squares
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if i == 0 and j == 0:
                                    continue
                                if ImprovedAgent.isValid(self, x + i, y + j):
                                    if self.agentBoard[x + i, y + j] == 'x':
                                        surHidSquares += 1
                                    elif self.agentBoard[x + i, y + j] == 'm':
                                        surMines += 1
                                    elif self.agentBoard[x + i, y + j].isdigit() \
                                            or self.safeSquareStack.contains(x + i, y + j):
                                        surSafeSquares += 1
                                else:
                                    surSafeSquares += 1

                        """print("currentSquare clue: ", int(clue))
                        print("surHidSquares: ", surHidSquares)
                        print("surMines: ", surMines)
                        print("surSafeSquares: ", surSafeSquares, "\n")"""

                        if 8 - int(clue) - surSafeSquares == surHidSquares \
                                or int(clue) == 0:  # Every hidden neighbor is safe
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    if ImprovedAgent.isValid(self, x + i, y + j):
                                        if self.agentBoard[x + i, y + j] == 'x' and not (x + i,
                                                                                         y + j) in self.safeSquareStack:
                                            self.safeSquareStack.append((x + i, y + j))

                        elif int(clue) - surMines == surHidSquares:  # Every hidden neighbor is a mine
                            # print("Every hidden neighbor is a mine")
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    if ImprovedAgent.isValid(self, x + i, y + j):
                                        if self.agentBoard[x + i, y + j] == 'x':
                                            # print("Labeling mine: (", x + i, ",", y + j, ")")
                                            self.agentBoard[x + i, y + j] = 'm'

                self.checkGameOver()
                if self.safeSquareStack:
                    currentSquare = self.safeSquareStack.pop()
                else:
                    """
                    Here is where the logic differs from the basic agent.
                    To avoid choosing a random mine, we will analyze squares that are adjacent to squares
                    with existing clues. We enumerate all possible mine configurations using this
                    data and choose the square that has the least number of configurations with it being a mine.
                    """
                    self.possibleMineSquares = []
                    for square in self.visitedSquares:
                        surHidSquares = 0
                        surMines = 0
                        surSafeSquares = 0
                        # print("SQUARE: ", square)
                        clue = self.gameBoard.board[square]
                        x = square[0]
                        y = square[1]
                        if clue.isdigit() and int(clue) > 0:
                            # Check surrounding squares
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    if ImprovedAgent.isValid(self, x + i, y + j):
                                        if self.agentBoard[x + i, y + j] == 'x':
                                            surHidSquares += 1
                                        elif self.agentBoard[x + i, y + j] == 'm':
                                            surMines += 1
                                        elif self.agentBoard[x + i, y + j].isdigit() \
                                                or self.safeSquareStack.contains(x + i, y + j):
                                            surSafeSquares += 1
                                    else:
                                        surSafeSquares += 1

                            """print("currentSquare clue: ", int(clue))
                            print("surHidSquares: ", surHidSquares)
                            print("surMines: ", surMines)
                            print("surSafeSquares: ", surSafeSquares, "\n")"""

                            if 8 - int(clue) - surSafeSquares < surHidSquares:  # Mine(s) are in the hidden squares
                                for i in range(-1, 2):
                                    for j in range(-1, 2):
                                        if i == 0 and j == 0:
                                            continue
                                        if ImprovedAgent.isValid(self, x + i, y + j):
                                            if self.agentBoard[x + i, y + j] == 'x':
                                                numCombinations = self.ncr(surHidSquares - 1, int(clue) - 1)
                                                for k in range(int(numCombinations)):
                                                    self.possibleMineSquares.append((x + i, y + j))

                    # End for loop. Count up results
                    counter = Counter(self.possibleMineSquares)
                    # print("possibleMineSquares Counter: ", counter)
                    if counter:
                        minSquare = min(Counter(self.possibleMineSquares), key=Counter(self.possibleMineSquares).get)
                        # print("minSquare: ", minSquare)
                        currentSquare = minSquare
                    else:
                        # print("CHOOSING RANDOM SQUARE")
                        randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                        randY = numpy.random.randint(low=0, high=self.gameBoard.dim)

                        while self.agentBoard[randX, randY] != 'x':
                            randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                            randY = numpy.random.randint(low=0, high=self.gameBoard.dim)
                        currentSquare = (randX, randY)

            self.clickSquare(currentSquare[0], currentSquare[1])
            if self.gameBoard.board[currentSquare] == 'm':
                # print("BOOOOOOOOOOOOOM")
                self.explosions += 1

            """
            # ----Print the current agentBoard----
            print("Turn ", turn, ":")
            print("Clicked Square: ", currentSquare)
            turn = turn + 1
            print(self.agentBoard)
            print(self.visitedSquares)
            print("\n\n")
            """
            self.checkGameOver()

    def clickSquare(self, x, y):
        self.agentBoard[x, y] = self.gameBoard.board[x, y]
        self.visitedSquares.append((x, y))
        return

    def checkGameOver(self):
        equal = self.agentBoard == self.gameBoard.board
        if equal.all():
            print("GAME OVER")
            print("gameBoard: \n", self.gameBoard.board)
            print("agentBoard: \n", self.agentBoard)
            print("Explosions: ", self.explosions)
            self.gameOver = True

    def ncr(self, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom

    def isValid(self, x, y):
        if x < 0 or y < 0 or (x > self.gameBoard.dim - 1) or y > (self.gameBoard.dim - 1):
            return False
        return True
