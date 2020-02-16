import Maze
import numpy


def setMazeOnFire(maze):
    while True:
        print("FIRE")
        fireSquare1 = numpy.random.choice(maze.dim)
        fireSquare2 = numpy.random.choice(maze.dim)
        if (maze.nums[fireSquare1][fireSquare2]) == 'E':
            maze.nums[fireSquare1][fireSquare2] = 'X'  # X represents a square on fire
            break


def printMaze(maze):
    for x in range(maze.nums.shape[0]):
        print("\n")
        for y in range(maze.nums.shape[1]):
            print(maze.nums[x][y], end="     ")


maze = Maze.Maze(5, 0.2)
setMazeOnFire(maze)
printMaze(maze)
#print("\n")
#print(aStarEuclid(maze))
#print(aStarManhattan(maze))