import os
import numpy


# -----------DFS-----------
def createMaze(dim, prob):
    size = dim
    nums = numpy.random.choice(['F', 'E'], size=(dim, dim), p=[prob, 1 - prob])
    nums[0, 0] = 'S'
    nums[dim - 1, dim - 1] = 'G'
    return nums


def dfs(maze):
    visited = {}
    stack = [[(0, 0)]]

    while stack:
        path = stack.pop()
        node = path[-1]
        visited[node] = 1
        if maze[node] == 'G':
            return path
        else:
            getNeighbors(maze, node[0], node[1], visited, stack, path)
    return "No path found"


def isValid(maze, x, y):
    if x < 0 or y < 0 or (x > maze.shape[0] - 1) or y > (maze.shape[1] - 1):
        return False
    if maze[x, y] == 'F' or maze[x, y] == 'S':
        return False
    return True


def getNeighbors(maze, x, y, visited, stack, pathO):
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
    return stack


# maze = createMaze(5, 0.2)
# print(dfs(maze))
# printMaze(maze)
# print(dfs(maze))

# -----------A Star-----------
def getEuclid(dim, x, y):
    a = (dim - 1 - x) ** 2
    b = (dim - 1 - y) ** 2
    return numpy.sqrt(a + b)


def getManhattan(dim, x, y):
    a = abs(dim - 1 - x)
    b = abs(dim - 1 - y)
    return a + b


def aStar(maze):
    dim = maze.size
    visited = {}

    # (x,x,x) represents (x coord, y coord, heuristic)
    # sortedList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0)]]
    heuristicList = [[(getEuclid(dim, 0, 0))]]
    while sortedList:
        path = sortedList.pop()
        pathHeuristic = heuristicList.pop()
        node = path[-1]
        visited[node] = 1
        if maze[node] == 'G':
            return path
        else:
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


def sortByHeuristic(sortedList):
    l = len(sortedList)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if sortedList[j][i] > sortedList[j + 1][1]:
                tempo = sortedList[j]
                sortedList[j] = sortedList[j + 1]
                sortedList[j + 1] = tempo
    print("sortedList", sortedList)
    return sortedList


def printMaze(self):
    for x in range(self.shape[0]):
        print("\n")
        for y in range(self.shape[1]):
            print(self[x][y], end=" ")


maze = createMaze(5, 0.2)
printMaze(maze)
print(aStar(maze))
