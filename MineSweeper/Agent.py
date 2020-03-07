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
        turn = 1
        self.gameBoard.printBoard()
        print("\n\n")

        # For the first turn we guess in the corner to optimize chances for solvability -coords (0,0)-
        self.clickSquare(0, 0)

        # Logic for basic agent loop:
        # 1) Iterate through list of safe squares and click on them, if they reveal more safe squares,
        # keep clicking until list is empty
        # 2) Identify mines and mark them

        while not self.gameOver:
            if self.safeSquareStack:  # If safeSquareStack is not empty, pop most recently added
                currentSquare = self.safeSquareStack.pop()
            else:  # If it is empty, that means no squares are guaranteed to be safe, so we need to
                # iterate through visited list and check if we can find any safe hidden squares
                # based on explored squares. If not, we choose at random
                for square in self.visitedSquares:
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
                                if Agent.isValid(self, x + i, y + j):
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
                            # print("Every hidden neighbor is safe")
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    if Agent.isValid(self, x + i, y + j):
                                        if self.agentBoard[x + i, y + j] == 'x' and not (x + i, y + j) in self.safeSquareStack:
                                            # print("APPENDING SAFESQUARES")
                                            self.safeSquareStack.append((x + i, y + j))

                        elif int(clue) - surMines == surHidSquares:  # Every hidden neighbor is a mine
                            # print("Every hidden neighbor is a mine")
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    if Agent.isValid(self, x + i, y + j):
                                        if self.agentBoard[x + i, y + j] == 'x':
                                            print("Labeling mine: (", x + i, ",", y+j, ")")
                                            self.agentBoard[x + i, y + j] = 'm'

                self.checkGameOver()
                if self.safeSquareStack:
                    currentSquare = self.safeSquareStack.pop()
                else:
                    print("CHOOSING RANDOM")
                    randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                    randY = numpy.random.randint(low=0, high=self.gameBoard.dim)

                    while self.agentBoard[randX, randY] != 'x':
                        randX = numpy.random.randint(low=0, high=self.gameBoard.dim)
                        randY = numpy.random.randint(low=0, high=self.gameBoard.dim)
                    currentSquare = (randX, randY)

            self.clickSquare(currentSquare[0], currentSquare[1])
            if self.gameBoard.board[currentSquare] == 'm':
                print("BOOOOOOOOOOOOOM")
            # ----Print the current agentBoard----
            print("Turn ", turn, ":")
            print("Clicked Square: ", currentSquare)
            turn = turn + 1
            print(self.agentBoard)
            print(self.visitedSquares)
            # print("CURRENT SAFESQUARESTACK: ", self.safeSquareStack, "\n")
            print("\n\n")
            self.checkGameOver()

            """clue = self.gameBoard.board[currentSquare]
            x = currentSquare[0]
            y = currentSquare[1]
            if clue != 'm':
                # Check surrounding squares
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

                print("currentSquare clue: ", int(clue))
                print("surHidSquares: ", surHidSquares)
                print("surMines: ", surMines)
                print("surSafeSquares: ", surSafeSquares, "\n")

                if int(clue) - surMines == surHidSquares:  # Every hidden neighbor is a mine
                    print("Every hidden neighbor is a mine")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if Agent.isValid(self, x + i, y + j):
                                if self.agentBoard[x + i, y + j] == 'x':
                                    self.agentBoard[x + i, y + j] = 'm'

                elif 8 - int(clue) - surSafeSquares == surHidSquares:  # Every hidden neighbor is safe
                    print("Every hidden neighbor is safe")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if Agent.isValid(self, x + i, y + j):
                                if self.agentBoard[x + i, y + j] == 'x' and not (x + i, y + j) in self.safeSquareStack:
                                    self.safeSquareStack.append((x + i, y + j))
            else:  # Current square is a mine
                self.agentBoard[x, y] = 'm'

            # ----Print the current agentBoard----
            print("Turn ", turn, ":")
            print("Clicked Square: ", currentSquare)
            turn = turn + 1
            print(self.agentBoard)
            print(self.visitedSquares)
            print("CURRENT SAFESQUARESTACK: ", self.safeSquareStack, "\n")"""

    def clickSquare(self, x, y):
        self.agentBoard[x, y] = self.gameBoard.board[x, y]
        self.visitedSquares.append((x, y))
        return

    def checkGameOver(self):
        equal = self.agentBoard == self.gameBoard.board
        if equal.all():
            print("Setting gameOver to True")
            print("gameBoard: \n", self.gameBoard.board)
            print("agentBoard: \n", self.agentBoard)
            self.gameOver = True

    def isValid(self, x, y):
        if x < 0 or y < 0 or (x > self.gameBoard.dim - 1) or y > (self.gameBoard.dim - 1):
            return False
        return True
