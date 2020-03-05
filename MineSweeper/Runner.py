from Board.py import Board

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
    maze.printMaze()

    #---------------Print out solutions here---------------