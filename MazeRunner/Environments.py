import os
import numpy


# depth first uses stack
def dfs(maze, currX, currY, visited, paths, stack):
    visited.append(currX, currY)
    if maze[currX, currY] == 'G':
        return visited


def checkNeighbors(maze, x, y, visited, stack):
    if edgeCheck(maze, x, y) == "top":
        if edgeCheck(maze, x, y) == "right":
            stack.push((x + 1, y))
            stack.push((x, y - 1))


def edgeCheck(maze, x, y):
    if x == 0:
        return "top"
    if x == maze.shape[0]:
        return "bottom"
    if y == 0:
        return "left"
    if y == maze.shape[1]:
        return "right"


#-----------A Star-----------
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


#-----------DFS-----------
def dfs(maze):
    visited = {}
    stack = [[(0, 0)]]
    i = 0
    while stack:
        path = stack.pop()
        node = path.pop()
        visited[i] = node
        if maze[node] == 'G':
            return path
        else:
            getNeighbors(maze, node[0], node[1], visited, stack, path)
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
        path1.append(x - 1, y)
        stack.append(path1)
    if isValid(maze, x, y - 1) and (x, y - 1) not in visited:
        path2 = pathO.copy()
        path2.append(x, y - 1)
        stack.append(path2)
    if isValid(maze, x + 1, y) and (x + 1, y) not in visited:
        path3 = pathO.copy()
        path3.append(x + 1, y)
        stack.append(path3)
    if isValid(maze, x, y + 1) and (x, y + 1) not in visited:
        path4 = pathO.copy()
        path4.append(x, y + 1)
        stack.append(path4)