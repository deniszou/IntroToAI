import os
import numpy


class Maze():
    def __init__(self, dim, prob):
        self.dim = dim
        self.prob = prob
        self.start = (0, 0)
        self.goal = (dim-1, dim-1)
        self.onFireList = []
        self.flammabilityRate = -1
        self.nums = numpy.random.choice(['F', 'E'], size=(dim, dim), p=[prob, 1 - prob])
        self.nums[0, 0] = 'S'
        self.nums[dim - 1, dim - 1] = 'G'

    def printMaze(self):
        for x in range(self.dim):
            print("\n")
            for y in range(self.dim):
                print(self.nums[x][y], end="      ")