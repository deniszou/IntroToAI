from Board import Board
from Agent import Agent

if __name__ == '__main__':
    # ---------------Create & print maze---------------
    dimension = int(input("What is the dimension of the board (Enter whole number)?\n"))
    while True:
        try:
            mines = int(input("Please enter a number of mines: "))
            break
        except mines >= dimension * dimension:
            print("Oops!  Invalid number of mines.  Try again...")
    board = Board(dimension, mines)
    board.printBoard()
    agent = Agent(board)

    #---------------Print out solutions here---------------