import numpy
import os


def createMaze(dim, prob):
    nums = numpy.random.choice(['F', 'E'], size=(dim, dim), p=[prob, 1 - prob])
    nums[0, 0] = 'S'
    nums[dim - 1, dim - 1] = 'G'

# depth first uses stack

def dfs(maze, currX, currY, visited, paths, stack):
    visited.append(currX, currY)
    if maze[currX, currY] == 'G'
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