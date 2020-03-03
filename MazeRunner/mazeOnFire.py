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
    while True:
        fireSquare1 = numpy.random.choice(maze.dim)
        fireSquare2 = numpy.random.choice(maze.dim)
        if (maze.nums[fireSquare1][fireSquare2]) == 'E':
            maze.nums[fireSquare1][fireSquare2] = 'X'  # X represents a square on fire

            # Check if the fire can be reached. If not, continue
            fireMaze = createMaze(maze, fireSquare2, fireSquare2)
            if Environments.dfs(fireMaze) == "No path found":
                print("Fire is unreachable")
                quit()

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
            if maze.nums[(x, y)] != 'F' and maze.nums[(x, y)] != 'X' and maze.nums[(x, y)] != 'G':
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
        maze.nums[toSetOnFire[x]] = 'X'


def isValid(maze, x, y):
    if x < 0 or y < 0 or (x > maze.dim - 1) or y > (maze.dim - 1):
        return False
    return True


def isValidStrategy1(maze, x, y):
    if x < 0 or y < 0 or (x > maze.shape[0] - 1) or y > (maze.shape[1] - 1):
        return False
    if maze[x, y] == 'F' or maze[x, y] == 'S':
        return False
    return True


# --------------------------Algorithms--------------------------
def getEuclid(dim, x, y):
    a = (dim - 1 - x) ** 2
    b = (dim - 1 - y) ** 2
    return numpy.sqrt(a + b)


def getFireEuclid(curTuple, fireTuple):
    (firex, firey) = fireTuple
    (curx, cury, curHeuristic) = curTuple
    a = (firex - 1 - curx) ** 2
    b = (firey - 1 - cury) ** 2
    return firex, firey, numpy.sqrt(a + b)


def findClosestFire(coords):
    fireEuclidList = []

    for x in range(len(maze.onFireList)):
        fireEuclidList.append(getFireEuclid(coords, maze.onFireList[x]))
        # Sort the fireEuclidList to find smallest distance
        # First element has the smallest distance
    fireEuclidList.sort(key=lambda z: z[2])
    (x, y, closestFire) = fireEuclidList[0]
    # print("FireEuclidList: ", fireEuclidList)
    # print("closestFire: ", closestFire)
    return closestFire


def findClosestFire3(coords):
    fireEuclidList = []

    for x in range(len(maze.onFireList)):
        (curx, cury) = maze.onFireList[x]
        fireEuclidList.append(getFireEuclid(coords, maze.onFireList[x]))
        # Spread the fire by one in each direction if possible
        if isValid(maze, curx - 1, cury) and maze.nums[curx - 1, cury] != 'F' and maze.nums[curx - 1, cury] != 'X' and \
                maze.nums[curx - 1, cury] != 'G':
            fireEuclidList.append(getFireEuclid(coords, (curx - 1, cury)))

        if isValid(maze, curx, cury - 1) and maze.nums[curx, cury - 1] != 'F' and maze.nums[curx, cury - 1] != 'X' and \
                maze.nums[curx, cury - 1] != 'G':
            fireEuclidList.append(getFireEuclid(coords, (curx, cury - 1)))

        if isValid(maze, curx + 1, cury) and maze.nums[curx + 1, cury] != 'F' and maze.nums[curx + 1, cury] != 'X' and \
                maze.nums[curx + 1, cury] != 'G':
            fireEuclidList.append(getFireEuclid(coords, (curx + 1, cury)))

        if isValid(maze, curx, cury + 1) and maze.nums[curx, cury + 1] != 'F' and maze.nums[curx, cury + 1] != 'X' and \
                maze.nums[curx, cury + 1] != 'G':
            fireEuclidList.append(getFireEuclid(coords, (curx, cury + 1)))

    # Sort the fireEuclidList to find smallest distance
    # First element has the smallest distance
    fireEuclidList.sort(key=lambda z: z[2])
    (x, y, closestFire) = fireEuclidList[0]
    return closestFire


# ---------------------------------Strategy 1---------------------------------
def aStarEuclidStrategy1(maze, flammability):
    setMazeOnFire(maze, flammability)
    printMaze(maze)
    dim = maze.dim
    visited = {}

    # heuristicList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0)]]
    heuristicList = [[(getEuclid(dim, 0, 0))]]
    while sortedList:
        printMaze(maze)
        path = sortedList.pop()
        pathHeuristic = heuristicList.pop()
        node = path[-1]
        visited[node] = 1

        if maze.nums[node] == 'G':
            print("Reached goal")
            print(path)
            return path
        if maze.nums[node] == 'X':
            print("You got burned")
            return path

        else:
            getNeighborsEuclid(maze.nums, node[0], node[1], visited, sortedList, heuristicList, path, dim)

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
        spreadFire(maze)

    return "No path found"


def getNeighborsEuclid(maze, x, y, visited, sortedList, heuristicList, pathO, dim):
    if isValidStrategy1(maze, x - 1, y) and visited.get((x - 1, y)) is None:
        path1 = pathO.copy()
        path1.append((x - 1, y))
        sortedList.append(path1)
        heuristicList.append(getEuclid(dim, x - 1, y))
    if isValidStrategy1(maze, x, y - 1) and visited.get((x, y - 1)) is None:
        path2 = pathO.copy()
        path2.append((x, y - 1))
        sortedList.append(path2)
        heuristicList.append(getEuclid(dim, x, y - 1))
    if isValidStrategy1(maze, x + 1, y) and visited.get((x + 1, y)) is None:
        path3 = pathO.copy()
        path3.append((x + 1, y))
        sortedList.append(path3)
        heuristicList.append(getEuclid(dim, x + 1, y))
    if isValidStrategy1(maze, x, y + 1) and visited.get((x, y + 1)) is None:
        path4 = pathO.copy()
        path4.append((x, y + 1))
        sortedList.append(path4)
        heuristicList.append(getEuclid(dim, x, y + 1))
    return sortedList, heuristicList


# ---------------------------------Strategy 2---------------------------------
def aStarEuclidStrategy2(maze, flammability):
    setMazeOnFire(maze, flammability)
    printMaze(maze)
    dim = maze.dim
    # heuristicList is sorted from highest to lowest heuristic
    path = [(0, 0, getEuclid(dim, 0, 0))]
    visited = []
    i = 0
    while True:
        i = i + 1
        printMaze(maze)
        curCoords = path[len(path) - 1]
        (curx, cury, curheuristic) = curCoords
        # print("curCoords: ", curCoords)

        curDistanceToFire = findClosestFire(curCoords)
        poss1CF = 0
        poss2CF = 0
        poss3CF = 0
        poss4CF = 0
        poss1h = 0
        poss2h = 0
        poss3h = 0
        poss4h = 0
        poss1x = 0
        poss1y = 0
        poss2x = 0
        poss2y = 0
        poss3x = 0
        poss3y = 0
        poss4x = 0
        poss4y = 0

        if i > 3 and visited[-1] == visited[len(visited)-3]:
            (a, b) = visited[-1]
            (c, d) = visited[-2]
            if a == c:
                if isValid(maze, curx - 1, cury) and maze.nums[curx - 1, cury] != 'F' and maze.nums[
                    curx - 1, cury] != 'X':
                    poss1 = (curx - 1, cury, getEuclid(dim, curx - 1, cury))
                    poss1CF = findClosestFire(poss1)
                    (poss1x, poss1y, poss1h) = poss1
                if isValid(maze, curx + 1, cury) and maze.nums[curx + 1, cury] != 'F' and maze.nums[
                    curx + 1, cury] != 'X':
                    poss3 = (curx + 1, cury, getEuclid(dim, curx + 1, cury))
                    poss3CF = findClosestFire(poss3)
                    (poss3x, poss3y, poss3h) = poss3
                if poss1CF == 0 and poss3CF == 0:
                    print("No possible moves")
                    print("PATH: ", path)
                    return "Dead"
                elif poss1CF != 0 or poss3CF != 0:
                    distanceToGoalDifferential1 = curheuristic - poss1h  # If this is positive, distance to goal decreased
                    distanceToGoalDifferential3 = curheuristic - poss3h
                    distanceToFireDifferential1 = int(
                        poss1CF) - curDistanceToFire  # If this is positive, distance to fire increased
                    distanceToFireDifferential3 = poss3CF - curDistanceToFire
                    if poss1CF == 0:
                        path.append(poss3)
                        visited.append((poss3x, poss3y))
                        continue
                    elif poss3CF == 0:
                        path.append(poss1)
                        visited.append((poss1x, poss1y))
                        continue

                    # Based on the sum of differentials, append either poss3 or poss4
                    elif distanceToFireDifferential1 + distanceToGoalDifferential1 > distanceToFireDifferential3 + distanceToGoalDifferential3:
                        path.append(poss1)
                        visited.append((poss1x, poss1y))
                        continue
                    else:
                        path.append(poss3)
                        visited.append((poss3x, poss3y))
                        continue
            elif b == d:
                if isValid(maze, curx, cury - 1) and maze.nums[curx, cury - 1] != 'F' and maze.nums[
                    curx, cury - 1] != 'X':
                    poss2 = (curx, cury - 1, getEuclid(dim, curx, cury - 1))
                    poss2CF = findClosestFire(poss2)
                    (poss2x, poss2y, poss2h) = poss2
                if isValid(maze, curx, cury + 1) and maze.nums[curx, cury + 1] != 'F' and maze.nums[
                    curx, cury + 1] != 'X':
                    poss4 = (curx, cury + 1, getEuclid(dim, curx, cury + 1))
                    poss4CF = findClosestFire(poss4)
                    (poss4x, poss4y, poss4h) = poss4
                if poss2CF == 0 and poss4CF == 0:
                    print("No possible moves")
                    print("PATH: ", path)
                    return "Dead"
                elif poss2CF != 0 or poss4CF != 0:
                    distanceToGoalDifferential2 = curheuristic - poss4h  # If this is positive, distance to goal decreased
                    distanceToGoalDifferential4 = curheuristic - poss4h
                    distanceToFireDifferential2 = int(
                        poss2CF) - curDistanceToFire  # If this is positive, distance to fire increased
                    distanceToFireDifferential4 = poss4CF - curDistanceToFire
                    if poss2CF == 0:
                        path.append(poss4)
                        visited.append((poss4x, poss4y))
                        continue
                    elif poss4CF == 0:
                        path.append(poss2)
                        visited.append((poss2x, poss2y))
                        continue

                    # Based on the sum of differentials, append either poss3 or poss4
                    elif distanceToFireDifferential2 + distanceToGoalDifferential2 > distanceToFireDifferential4 + distanceToGoalDifferential4:
                        path.append(poss2)
                        visited.append((poss2x, poss2y))
                        continue
                    else:
                        path.append(poss4)
                        visited.append((poss4x, poss4y))
                        continue

        if path[len(path) - 1] == 'X':
            print("You got burned")
            print("PATH: ", path)
            return path

        if dim - 1 == curx and dim - 1 == cury:
            print("Goal reached")
            print("PATH: ", path)
            return path

        else:
            # Get potential moves and their heuristic
            if isValid(maze, curx - 1, cury) and maze.nums[curx - 1, cury] != 'F' and maze.nums[curx - 1, cury] != 'X':
                poss1 = (curx - 1, cury, getEuclid(dim, curx - 1, cury))
                poss1CF = findClosestFire(poss1)
                (poss1x, poss1y, poss1h) = poss1

            if isValid(maze, curx, cury - 1) and maze.nums[curx, cury - 1] != 'F' and maze.nums[curx, cury - 1] != 'X':
                poss2 = (curx, cury - 1, getEuclid(dim, curx, cury - 1))
                poss2CF = findClosestFire(poss2)
                (poss2x, poss2y, poss2h) = poss2

            if isValid(maze, curx + 1, cury) and maze.nums[curx + 1, cury] != 'F' and maze.nums[curx + 1, cury] != 'X':
                poss3 = (curx + 1, cury, getEuclid(dim, curx + 1, cury))
                poss3CF = findClosestFire(poss3)
                (poss3x, poss3y, poss3h) = poss3

            if isValid(maze, curx, cury + 1) and maze.nums[curx, cury + 1] != 'F' and maze.nums[curx, cury + 1] != 'X':
                poss4 = (curx, cury + 1, getEuclid(dim, curx, cury + 1))
                poss4CF = findClosestFire(poss4)
                (poss4x, poss4y, poss4h) = poss4

            # If all equal zero, there are no moves left
            if poss1CF == 0 and poss2CF == 0 and poss3CF == 0 and poss4CF == 0:
                print("No possible moves")
                print("PATH: ", path)
                return "Dead"

            # Weigh heuristicList's distance vs fireEuclidList's distance and choose next move
            # Avoid moving left or up because we are on a time constraint unless we have to
            if poss3CF != 0 or poss4CF != 0:
                distanceToGoalDifferential3 = curheuristic - poss3h  # If this is positive, distance to goal decreased
                distanceToGoalDifferential4 = curheuristic - poss4h
                distanceToFireDifferential3 = int(
                    poss3CF) - curDistanceToFire  # If this is positive, distance to fire increased
                distanceToFireDifferential4 = poss4CF - curDistanceToFire
                if poss3CF == 0:
                    path.append(poss4)
                    visited.append((poss4x, poss4y))
                    continue
                elif poss4CF == 0:
                    path.append(poss3)
                    visited.append((poss3x, poss3y))
                    continue

                # Based on the sum of differentials, append either poss3 or poss4
                elif distanceToFireDifferential3 + distanceToGoalDifferential3 > distanceToFireDifferential4 + distanceToGoalDifferential4:
                    path.append(poss3)
                    visited.append((poss3x, poss3y))
                    continue
                else:
                    path.append(poss4)
                    visited.append((poss4x, poss4y))
                    continue

            # Not possible so have to go left or right
            elif poss1CF != 0 or poss2CF != 0:
                distanceToGoalDifferential1 = curheuristic - poss1h  # If this is positive, distance to goal decreased
                distanceToGoalDifferential2 = curheuristic - poss2h
                distanceToFireDifferential1 = int(
                    poss1CF) - curDistanceToFire  # If this is positive, distance to fire increased
                distanceToFireDifferential2 = poss2CF - curDistanceToFire
                if poss1CF == 0:
                    path.append(poss2)
                    visited.append((poss2x, poss2y))
                    continue
                elif poss3CF == 0:
                    path.append(poss1)
                    visited.append((poss1x, poss1y))
                    continue

                # Based on the sum of differentials, append either poss3 or poss4
                elif distanceToFireDifferential1 + distanceToGoalDifferential1 > distanceToFireDifferential2 + distanceToGoalDifferential2:
                    path.append(poss1)
                    visited.append((poss1x, poss1y))
                    continue
                else:
                    path.append(poss2)
                    visited.append((poss2x, poss3y))
                    continue

        spreadFire(maze)


    return "No path found"


# ---------------------------------Strategy 3---------------------------------
def aStarEuclidStrategy3(maze, flammability):
    setMazeOnFire(maze, flammability)
    printMaze(maze)
    dim = maze.dim
    # heuristicList is sorted from highest to lowest heuristic
    path = [(0, 0, getEuclid(dim, 0, 0))]
    while True:
        printMaze(maze)
        curCoords = path[len(path) - 1]
        (curx, cury, curheuristic) = curCoords
        print("curCoords: ", curCoords)

        curDistanceToFire = findClosestFire3(curCoords)
        poss1CF = 0
        poss2CF = 0
        poss3CF = 0
        poss4CF = 0
        poss1h = 0
        poss2h = 0
        poss3h = 0
        poss4h = 0

        if path[len(path) - 1] == 'X':
            print("You got burned")
            print("PATH: ", path)
            return path

        if dim - 1 == curx and dim - 1 == cury:
            print("Goal reached")
            print("PATH: ", path)
            return path

        else:
            # Get potential moves and their heuristic
            if isValid(maze, curx - 1, cury) and maze.nums[curx - 1, cury] != 'F' and maze.nums[curx - 1, cury] != 'X':
                poss1 = (curx - 1, cury, getEuclid(dim, curx - 1, cury))
                poss1CF = findClosestFire(poss1)
                (poss1x, poss1y, poss1h) = poss1

            if isValid(maze, curx, cury - 1) and maze.nums[curx, cury - 1] != 'F' and maze.nums[curx, cury - 1] != 'X':
                poss2 = (curx, cury - 1, getEuclid(dim, curx, cury - 1))
                poss2CF = findClosestFire(poss2)
                (poss2x, poss2y, poss2h) = poss2

            if isValid(maze, curx + 1, cury) and maze.nums[curx + 1, cury] != 'F' and maze.nums[curx + 1, cury] != 'X':
                poss3 = (curx + 1, cury, getEuclid(dim, curx + 1, cury))
                poss3CF = findClosestFire(poss3)
                (poss3x, poss3y, poss3h) = poss3

            if isValid(maze, curx, cury + 1) and maze.nums[curx, cury + 1] != 'F' and maze.nums[curx, cury + 1] != 'X':
                poss4 = (curx, cury + 1, getEuclid(dim, curx, cury + 1))
                poss4CF = findClosestFire(poss4)
                (poss4x, poss4y, poss4h) = poss4

            # If all equal zero, there are no moves left
            if poss1CF == 0 and poss2CF == 0 and poss3CF == 0 and poss4CF == 0:
                print("No possible moves")
                print("PATH: ", path)
                return "Dead"

            # Weigh heuristicList's distance vs fireEuclidList's distance and choose next move
            # Avoid moving left or up because we are on a time constraint unless we have to
            if poss3CF != 0 or poss4CF != 0:
                distanceToGoalDifferential3 = curheuristic - poss3h  # If this is positive, distance to goal decreased
                distanceToGoalDifferential4 = curheuristic - poss4h
                distanceToFireDifferential3 = int(
                    poss3CF) - curDistanceToFire  # If this is positive, distance to fire increased
                distanceToFireDifferential4 = poss4CF - curDistanceToFire
                if poss3CF == 0:
                    path.append(poss4)
                elif poss4CF == 0:
                    path.append(poss3)

                # Based on the sum of differentials, append either poss3 or poss4
                elif distanceToFireDifferential3 + distanceToGoalDifferential3 > distanceToFireDifferential4 + distanceToGoalDifferential4:
                    path.append(poss3)
                else:
                    path.append(poss4)

            # Not possible so have to go left or right
            elif poss1CF != 0 or poss2CF != 0:
                distanceToGoalDifferential1 = curheuristic - poss1h  # If this is positive, distance to goal decreased
                distanceToGoalDifferential2 = curheuristic - poss2h
                distanceToFireDifferential1 = int(
                    poss1CF) - curDistanceToFire  # If this is positive, distance to fire increased
                distanceToFireDifferential2 = poss2CF - curDistanceToFire
                if poss1CF == 0:
                    path.append(poss2)
                elif poss2CF == 0:
                    path.append(poss1)

                # Based on the sum of differentials, append either poss3 or poss4
                elif distanceToFireDifferential1 + distanceToGoalDifferential1 > distanceToFireDifferential2 + distanceToGoalDifferential2:
                    path.append(poss1)
                else:
                    path.append(poss2)

        spreadFire(maze)

    return "No path found"


def printMaze(maze):
    for x in range(maze.nums.shape[0]):
        print("\n")
        for y in range(maze.nums.shape[1]):
            print(maze.nums[x][y], end="     ")


# ------------------------Testing------------------------
maze = Maze.Maze(5, 0.2)
aStarEuclidStrategy1(maze, 0.1)
aStarEuclidStrategy2(maze, 0.1)
aStarEuclidStrategy3(maze, 0.1)
