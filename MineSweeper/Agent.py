from Game import Game
import numpy


# This class will be used to play the game on Agent's own board
class Agent:
    def __init__(self, board):
        self.gameOver = False
        self.gameBoard = board
        self.agentBoard = numpy.full((board.dim, board.dim), 'x')
        self.visitedSquares = []
        self.safeSquareStack = []

    def play(self):
        print("Playing Game...")
        i = 2
        self.gameBoard.printBoard()

        # For the first turn we guess in the corner to optimize chances for solvability -coords (0,0)-
        self.clickSquare(0, 0)
        print("Turn 1: ")
        print(self.agentBoard)
        print(self.visitedSquares)

        # Logic for basic agent loop:
        # 1) Iterate through list of safe squares and click on them, if they reveal more safe squares,
        # keep clicking until list is empty
        # 2) Identify mines and mark them

        while not self.gameOver:
            print("Turn ", i, ":")
            print(self.agentBoard)
            print(self.visitedSquares)
            currentSquare = (-1, -1)

            if self.safeSquareStack:  # If safeSquareStack is not empty, pop most recently added
                currentSquare = self.safeSquareStack.pop()
            else:  # If it is empty, that means no squares are guaranteed to be safe, so choose random
                randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                randY = numpy.random.randint(low=0, high=self.gameBoard.dim)

                while self.agentBoard[randX, randY] != 'x':
                    randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                    randY = numpy.random.randint(low=0, high=self.gameBoard.dim)
                self.clickSquare(randX, randY)

            clue = self.agentBoard[currentSquare]
            print(clue)
            surHidSquares = 0
            surMines = 0
            surSafeSquares = 0

            if clue != 'm':
                # Check surrounding squares
                x = currentSquare[0]
                y = currentSquare[1]
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if Agent.isValid(self, x + i, y + j):
                            if self.agentBoard[x + i, y + j] == 'x':
                                surHidSquares += 1
                            elif self.agentBoard[x + i, y + j] == 'm':
                                surMines += 1
                            elif self.agentBoard[x + i, y + j].isdigit() or self.safeSquareStack.contains(x + i, y + j):
                                surSafeSquares += 1
                        else:
                            surSafeSquares += 1

                print("surHidSquares: ", surHidSquares)
                print("surMines: ", surMines)
                print("surSafeSquares: ", surSafeSquares)

                if ord(clue) - surMines == surHidSquares:  # Every hidden neighbor is a mine
                    print("Every hidden neighbor is mine")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if Agent.isValid(self, x + i, y + j):
                                if self.agentBoard[x + i, y + j] == 'x':
                                    self.agentBoard[x + i, y + j] = 'm'

                elif 8 - ord(clue) - surSafeSquares == surHidSquares:  # Every hidden neighbor is safe
                    print("Every hidden neighbor is safe")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if Agent.isValid(self, x + i, y + j):
                                if self.agentBoard[x + i, y + j] == 'x':
                                    self.safeSquareStack.append(x, y)

    def clickSquare(self, x, y):
        self.agentBoard[x, y] = self.gameBoard.board[x, y]
        self.visitedSquares.append((x, y))
        return

    def isValid(self, x, y):
        if x < 0 or y < 0 or (x > self.gameBoard.dim - 1) or y > (self.gameBoard.dim - 1):
            return False
        return True
