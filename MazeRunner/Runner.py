from Maze import Maze
import Environments

if __name__ == '__main__':
    # ---------------Create & print maze---------------
    dimension = int(input("What is the demnsion of the maze (Enter whole number)?\n"))
    percent = float(input("What is the percentage chance a space is filled (Enter between 0 and 1)?\n"))
    maze = Maze(dimension, percent)
    maze.printMaze()

    #---------------Print out solutions here---------------
    Environments.dfs(maze)