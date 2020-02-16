import os
import numpy


# -----------DFS-----------
def createMaze(dim, prob):
    nums = numpy.random.choice(['F', 'E'], size=(dim, dim), p=[prob, 1 - prob])
    nums[0, 0] = 'S'
    nums[dim - 1, dim - 1] = 'G'
    return nums


def dfs(maze):
    visited = {}
    stack = [[(0, 0)]]
    i = 0
    while stack:
        path = stack.pop()
        node = path.pop()
        visited[i] = node
        if maze.nums[node] == 'G':
            return path
        else:
            getNeighbors(maze.nums, node[0], node[1], visited, stack, path)
        i += 1


def isValid(maze, x, y):
    if x < 0 or y < 0 or (x > maze.shape[0] - 1) or y > (maze.shape[1] - 1):
        return False
    if maze[x, y] == 'F' or maze[x, y] == 'S':
        return False
    return True


def getNeighbors(maze, x, y, visited, stack, pathO):
    if isValid(maze, x - 1, y) and (x - 1, y) not in visited:
        path1 = pathO.copy()
        path1.append((x - 1, y))
        stack.append(path1)
    if isValid(maze, x, y - 1) and (x, y - 1) not in visited:
        path2 = pathO.copy()
        path2.append((x, y - 1))
        stack.append(path2)
    if isValid(maze, x + 1, y) and (x + 1, y) not in visited:
        path3 = pathO.copy()
        path3.append((x + 1, y))
        stack.append(path3)
    if isValid(maze, x, y + 1) and (x, y + 1) not in visited:
        path4 = pathO.copy()
        path4.append((x, y + 1))
        stack.append(path4)
    return stack


def printMaze(self):
    for x in range(self.shape[0]):
        print("\n")
        for y in range(self.shape[1]):
            print(self[x][y], end=" ")


maze = createMaze(10, 0.3)
print(dfs(maze))
printMaze(maze)
print(dfs(maze))


# -----------A Star-----------
def getEuclid(self, dim, x, y):
    a = (dim - 1 - x) ** 2
    b = (dim - 1 - y) ** 2
    return numpy.sqrt(a + b)


def getManhattan(self, dim, x, y):
    a = abs(dim - 1 - x)
    b = abs(dim - 1 - y)
    return a + b


def aStar(maze, self):
    dim = maze.dim
    visited = {}

    # (x,x,x) represents (x coord, y coord, heuristic)
    # sortedList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0, 0)]]
    i = 0
    while sortedList:
        path = sortedList.pop()
        node = path.pop()
        visited[i] = node
        if maze[node] == 'G':
            return path
        else:
            getNeighborsAStar(maze, node[0], node[1], visited, sortedList, path, dim)
            sortedList = sortByHeuristic(sortedList)
        i += 1


def getNeighborsAStar(maze, x, y, visited, sortedList, pathO, dim):
    if isValid(maze, x - 1, y) and (x - 1, y) not in visited:
        path1 = pathO.copy()
        path1.append(x - 1, y, getEuclid(dim, x - 1, y))
        sortedList.append(path1)
    if isValid(maze, x, y - 1) and (x, y - 1) not in visited:
        path2 = pathO.copy()
        path2.append(x, y - 1, getEuclid(dim, x, y - 1))
        sortedList.append(path2)
    if isValid(maze, x + 1, y) and (x + 1, y) not in visited:
        path3 = pathO.copy()
        path3.append(x + 1, y, getEuclid(dim, x + 1, y))
        sortedList.append(path3)
    if isValid(maze, x, y + 1) and (x, y + 1) not in visited:
        path4 = pathO.copy()
        path4.append(x, y + 1, getEuclid(dim, x, y + 1))
        sortedList.append(path4)


def sortByHeuristic(sortedList):
    l = len(sortedList)
    for i in range(0,l):
        for j in range(0, l-i-1):
            if sortedList[j][i] > sortedList[j + 1][1]:
                tempo = sortedList[j]
                sortedList[j] = sortedList[j+1]
                sortedList[j+1] = tempo
    return sortedList

