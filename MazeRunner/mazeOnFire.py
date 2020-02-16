import Maze
import Environments
import numpy


def createMaze(maze, x, y):
    nums = numpy.copy(maze.nums)
    nums[0, 0] = 'S'
    nums[x, y] = 'G'
    return nums


def setMazeOnFire(maze, flammabilityRate):
    maze.flammabilityRate = flammabilityRate
    print("Flamrate: ", flammabilityRate)
    while True:
        print("FIRE")
        fireSquare1 = numpy.random.choice(maze.dim)
        fireSquare2 = numpy.random.choice(maze.dim)
        if (maze.nums[fireSquare1][fireSquare2]) == 'E':
            maze.nums[fireSquare1][fireSquare2] = 'X'  # X represents a square on fire

            # Check if the fire can be reached. If not, continue
            fireMaze = createMaze(maze, fireSquare2, fireSquare2)
            if Environments.dfs(fireMaze) == "No path found":
                print("Fire is unreachable")
                return

            maze.onFireList.append((fireSquare1, fireSquare2))
            print("onFireList1111: ", maze.onFireList)
            break


def spreadFire(maze):
    print("\nSPREADING FIRE")
    toSetOnFire = []
    # Check every square for fires around it
    for x in range(maze.dim):
        for y in range(maze.dim):
            k = 0
            if maze.nums[(x, y)] == 'E':
                # print("[", x, ",", y, "]")
                if isValid(maze, x - 1, y) and maze.nums[x - 1, y] == 'X':
                    k = k + 1
                if isValid(maze, x, y - 1) and maze.nums[x, y - 1] == 'X':
                    k = k + 1
                if isValid(maze, x + 1, y) and maze.nums[x + 1, y] == 'X':
                    k = k + 1
                if isValid(maze, x, y + 1) and maze.nums[x, y + 1] == 'X':
                    k = k + 1

                # print("K: ", k)
                if k > 0:
                    fireProb = 1 - (1 - maze.flammabilityRate) ** k
                    result = numpy.random.choice(('X', 'E'), size=1, p=[fireProb, 1 - fireProb])
                    print("RESULT: ", result)
                    if result == 'X':
                        toSetOnFire.append((x, y))
                        maze.onFireList.append((x, y))

                else:
                    continue
            else:
                continue
    # Have to wait to the end to set squares on fire or else they will influence
    # the probabilities while iterating through
    for x in range(len(toSetOnFire)):
        print("tosetonfire: ", toSetOnFire[x])
        maze.nums[toSetOnFire[x]] = 'X'


def isValid(maze, x, y):
    if x < 0 or y < 0 or (x > maze.dim - 1) or y > (maze.dim - 1):
        return False
    return True


def getEuclid(dim, x, y):
    a = (dim - 1 - x) ** 2
    b = (dim - 1 - y) ** 2
    return numpy.sqrt(a + b)


def getFireEuclid(fireTuple, curTuple):
    (firex, firey) = fireTuple
    (curx, cury) = curTuple
    a = (firex - 1 - curx) ** 2
    b = (firey - 1 - cury) ** 2
    return numpy.sqrt(a + b)


def aStarEuclid(maze):
    setMazeOnFire(maze, 0.5)
    dim = maze.dim
    visited = {}

    # heuristicList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0)]]
    heuristicList = [[(getEuclid(dim, 0, 0))]]
    while sortedList:
        path = sortedList.pop()
        curCoords = path[len(path) - 1]
        print("curCoords: ", curCoords)
        pathHeuristic = heuristicList.pop()
        node = path[-1]
        visited[node] = 1
        if maze.nums[node] == 'G':
            return path
        else:
            # Check to see which fire square is closest to the current position
            print("onFireList: ", maze.onFireList)
            for x in range(len(maze.onFireList)):
                getFireEuclid(maze.onFireList[x], curCoords)

            getNeighborsEuclid(maze, node[0], node[1], visited, sortedList, heuristicList, path, dim)

            # Sort sortedList and heuristicList by heuristic (Insertion sort)
            for i in range(len(heuristicList)):
                cursor = heuristicList[i]
                pos = i

                while pos > 0 and heuristicList[pos - 1] < cursor:
                    # Swap the number down the list
                    heuristicList[pos] = heuristicList[pos - 1]
                    sortedList[pos] = sortedList[pos - 1]
                    pos = pos - 1
                # Break and do the final swap
                heuristicList[pos] = cursor

    return "No path found"


def getNeighborsEuclid(maze, x, y, visited, sortedList, heuristicList, pathO, dim):
    if isValid(maze, x - 1, y) and visited.get((x - 1, y)) is None:
        path1 = pathO.copy()
        path1.append((x - 1, y))
        sortedList.append(path1)
        heuristicList.append(getEuclid(dim, x - 1, y))
    if isValid(maze, x, y - 1) and visited.get((x, y - 1)) is None:
        path2 = pathO.copy()
        path2.append((x, y - 1))
        sortedList.append(path2)
        heuristicList.append(getEuclid(dim, x, y - 1))
    if isValid(maze, x + 1, y) and visited.get((x + 1, y)) is None:
        path3 = pathO.copy()
        path3.append((x + 1, y))
        sortedList.append(path3)
        heuristicList.append(getEuclid(dim, x + 1, y))
    if isValid(maze, x, y + 1) and visited.get((x, y + 1)) is None:
        path4 = pathO.copy()
        path4.append((x, y + 1))
        sortedList.append(path4)
        heuristicList.append(getEuclid(dim, x, y + 1))
    return sortedList, heuristicList


def printMaze(maze):
    for x in range(maze.nums.shape[0]):
        print("\n")
        for y in range(maze.nums.shape[1]):
            print(maze.nums[x][y], end="     ")


maze = Maze.Maze(5, 0.6)
aStarEuclid(maze)
printMaze(maze)
