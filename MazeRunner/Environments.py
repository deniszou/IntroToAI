import numpy
import os


def createMaze(dim, prob):
    nums = numpy.random.choice(['F', 'E'], size=(dim, dim), p=[prob, 1 - prob])
    nums[0, 0] = 'S'
    nums[dim - 1, dim - 1] = 'G'

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

