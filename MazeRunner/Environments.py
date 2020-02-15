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
