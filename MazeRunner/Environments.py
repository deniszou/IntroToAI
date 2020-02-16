import numpy
import os


def createMaze(dim, prob):
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


def printMaze(self):
    for x in range(self.shape[0]):
        print("\n")
        for y in range(self.shape[1]):
            print(self[x][y], end=" ")


maze = createMaze(30, 0.9)
print(dfs(maze))
printMaze(maze)
print(dfs(maze))
