import numpy
import copy

import Maze


def dfs(maze, harder=False):
    visited = {}
    stack = [[(0, 0)]]

    while stack:
        path = stack.pop()
        node = path[-1]
        visited[node] = 1
        if maze.nums[node] == 'G':
            return path
        else:
            getNeighbors(maze, node[0], node[1], visited, stack, path, harder)
    return "No path found"


def hardDfs(maze, harder=False):
    visited = {}
    stack = [[(0, 0)]]

    while stack:
        path = stack.pop()
        node = path[-1]
        visited[node] = 1
        if maze.nums[node] == 'G':
            return path
        else:
            getNeighbors(maze, node[0], node[1], visited, stack, path, harder)
    return "No path found"


def isValid(maze, x, y):
    if x < 0 or y < 0 or (x > maze.nums.shape[0] - 1) or y > (maze.nums.shape[1] - 1):
        return False

    #    if harder:
    #        flip(maze, x, y)

    if maze.nums[x, y] == 'F' or maze.nums[x, y] == 'S':
        return False
    return True


def isValidHelper(maze, x, y):
    if x < 0 or y < 0 or (x > maze.nums.shape[0] - 1) or y > (maze.nums.shape[1] - 1):
        return False
    return True


def flip(maze, x, y):
    if maze.nums[x, y] == 'F':
        maze.nums[x, y] = 'E'
    if maze.nums[x, y] == 'E':
        maze.nums[x, y] = 'F'


def checkMaze2(maze2, x, y, maze, visited, maze3, maze4):
    if isValidHelper(maze2, x, y - 1) and visited.get((x, y - 1)) is None:
        maze2.fringeSize = 0
        flip(maze2, x, y - 1)
        hardDfs(maze2)
        if hardDfs(maze2) == "No path found" or maze2.fringeSize <= maze.maxFringe:
            checkMaze3(maze3, x, y, maze, visited, maze4)
        elif maze2.fringeSize > maze.maxFringe:
            maze.maxFringe = maze2.fringeSize
            return 2
    else:
        checkMaze3(maze3, x, y, maze, visited, maze4)


def checkMaze3(maze3, x, y, maze, visited, maze4):
    if isValidHelper(maze3, x + 1, y) and visited.get((x + 1, y)) is None:
        maze3.fringeSize = 0
        flip(maze3, x + 1, y)
        hardDfs(maze3)
        if hardDfs(maze3) == "No path found" or maze3.fringeSize <= maze.maxFringe:
            checkMaze4(maze4, x, y, maze, visited)
        elif maze3.fringeSize > maze.maxFringe:
            maze.maxFringe = maze3.fringeSize
            return 3
    else:
        checkMaze4(maze4, x, y, maze, visited)


def checkMaze4(maze4, x, y, maze, visited):
    if isValidHelper(maze4, x, y + 1) and visited.get((x, y + 1)) is None:
        maze4.fringeSize = 0
        flip(maze4, x, y - 1)
        hardDfs(maze4)
        if hardDfs(maze4) == "No path found" or maze4.fringeSize <= maze.maxFringe:
            return 'f'
        elif maze4.fringeSize > maze.maxFringe:
            maze.maxFringe = maze4.fringeSize
            return 4
    return 0


def getNeighbors(maze, x, y, visited, stack, pathO, harder=False):
    if harder:
        maze1 = copy.deepcopy(maze)
        maze2 = copy.deepcopy(maze)
        maze3 = copy.deepcopy(maze)
        maze4 = copy.deepcopy(maze)
        if isValidHelper(maze1, x - 1, y) and visited.get((x - 1, y)) is None:
            maze1.fringeSize = 0
            flip(maze1, x - 1, y)
            hardDfs(maze1)
            if hardDfs(maze1) == "No path found" or maze1.fringeSize <= maze.maxFringe:
                a = checkMaze2(maze2, x, y, maze, visited, maze3, maze4)
                if a == 0:
                    maze = maze
                if a == 2:
                    maze = maze2
                if a == 3:
                    maze = maze3
                if a == 4:
                    maze = maze4
            elif maze1.fringeSize > maze.maxFringe:
                maze.maxFringe = maze1.fringeSize
                maze = maze1
        else:
            a = checkMaze2(maze2, x, y, maze, visited, maze3, maze4)
            a = checkMaze2(maze2, x, y, maze, visited, maze3, maze4)
            if a == 0:
                maze = maze
            if a == 2:
                maze = maze2
            if a == 3:
                maze = maze3
            if a == 4:
                maze = maze4
    if isValid(maze, x - 1, y) and visited.get((x - 1, y)) is None:
        path1 = pathO.copy()
        path1.append((x - 1, y))
        stack.append(path1)
    if isValid(maze, x, y - 1) and visited.get((x, y - 1)) is None:
        path2 = pathO.copy()
        path2.append((x, y - 1))
        stack.append(path2)
    if isValid(maze, x + 1, y) and visited.get((x + 1, y)) is None:
        path3 = pathO.copy()
        path3.append((x + 1, y))
        stack.append(path3)
    if isValid(maze, x, y + 1) and visited.get((x, y + 1)) is None:
        path4 = pathO.copy()
        path4.append((x, y + 1))
        stack.append(path4)
    if len(stack) > maze.fringeSize:
        maze.fringeSize = len(stack)
    return stack


def generateMaze(maze):
    dfs(maze)
    maze.maxFringe = maze.fringeSize
    print("original maze \n")
    maze.printMaze()
    hard = True
    print("\n")
    dfs(maze, hard)
    print("hard maze \n")
    maze.printMaze()


firstMaze = Maze.Maze(7, 0.3)
while dfs(firstMaze) == "No path found":
    firstMaze = Maze.Maze(7, 0.3)
generateMaze(firstMaze)
