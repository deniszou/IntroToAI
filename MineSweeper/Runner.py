from Board import Board
from Agent import Agent
from ImprovedAgent import ImprovedAgent

if __name__ == '__main__':
    # ---------------Create & print maze---------------
    """ dimension = int(input("What is the dimension of the board (Enter whole number)?  "))
    while True:
        try:
            mines = int(input("Please enter a number of mines: "))
            break
        except mines >= dimension * dimension:
            print("Oops!  Invalid number of mines.  Try again...") """
    # board = Board(dimension, mines)
    board = Board(50, 1000)
    board.printBoard()
    agent1 = Agent(board)
    agent2 = ImprovedAgent(board)
    agent1.play()
    agent2.play()

    #---------------Print out solutions here---------------