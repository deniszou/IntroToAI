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

    while stack:
        # print("STACK", stack)
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

# -----------Breadth First Search (BFS)-----------
def bfs(maze, start=(0,0)):
    # goal is bottom most right most square
    goal=(len(maze)-1, len(maze)-1)
    # keeps track of discovered nodes and their parents
    prev = {}
    # fringe data structure is a queue (first in first out)
    fringe = [start]
    # keeps track of visited nodes so that we don't infinite loop
    visited_set = [start]
    # root node has no parent
    prev[start] = None
    
    # while we have nodes still to discover
    while len(fringe) != 0:
        # get the node from the front of the queue
        curr_state = fringe.pop(0)
        # CHECK FOR GOAL STATE; goal state is (len(maze)-1, len(maze)-1) 
        if curr_state == goal:
            # array to store the final path (SOLUTION)
            path = [goal]
            state = goal
            # traverse backwards in prev to find the parents and add to the solution
            while state != (0,0):
                state = prev[state]
                path.insert(0, state)
            return path
        # add any valid children (not discovered yet and isn't out of bounds or isn't a wall)
        addValidChildren(maze, fringe, curr_state, prev, visited_set)
    return "No Solution"

def addValidChildren(maze, fringe, parent, prev, visited):
    # for each children, check that the children isn't out of bounds and isn't visited and isn't a wall
    # left child
    if parent[1] - 1 >= 0 and maze[parent[0]][parent[1]-1] != 'F' and (parent[0], parent[1]-1) not in visited:
        child = (parent[0], parent[1]-1)
        fringe.append(child)
        visited.append(child)
        prev[child] = parent
    # top child
    if parent[0] - 1 >= 0 and maze[parent[0]-1][parent[1]] != 'F' and (parent[0]-1, parent[1]) not in visited:
        child = (parent[0]-1, parent[1])
        fringe.append(child)
        visited.append(child)
        prev[child] = parent
    # right child
    if parent[1] + 1 < len(maze) and maze[parent[0]][parent[1]+1] != 'F' and (parent[0], parent[1]+1) not in visited:
        child = (parent[0], parent[1]+1)
        fringe.append(child)
        visited.append(child)
        prev[child] = parent
    # bottom child
    if parent[0] + 1 < len(maze) and maze[parent[0]+1][parent[1]] != 'F' and (parent[0]+1,parent[1]) not in visited:
        child = (parent[0]+1,parent[1])
        fringe.append(child)
        visited.append(child)
        prev[child] = parent         
# -----------Bidirectional BFS-----------
def bidirectional_bfs(maze):
    # roots of each BFS tree
    root_g = (len(maze)-1, len(maze)-1)
    root_s = (0,0)

    # two dictionaries to keep track of discovered nodes of each tree and their parents
    prev_s = {}
    prev_g = {}
    
    # two queues for each bfs tree
    fringe_s = [root_s]
    fringe_g = [root_g]

    # keep track of visited nodes for each tree
    visited_s = [root_s]
    visited_g = [root_g]

    # no parents for root nodes
    prev_s[root_s] = None
    prev_g[root_g] = None

    while len(fringe_s) != 0 and len(fringe_g) != 0:
        curr_state_s = fringe_s.pop(0)
        curr_state_g = fringe_g.pop(0)
        
        # CHECK FOR GOAL STATE (A MIDDLE GROUND NODE THAT HAS ALREADY BEEN DISCOVERED IN THE OTHER TREE OR IF BOTH CURRENT NODES ARE THE SAME)
        if curr_state_s == curr_state_g or curr_state_s in prev_g or curr_state_g in prev_s:
            # if curr_state_s is in both fringes there is an intersection/complete path
            if(curr_state_s in prev_g):
                path = [curr_state_s]
                # set initial states
                state_s = curr_state_s
                state_g = curr_state_s
            # if curr_state_g is in both fringes there is an intersection/complete path
            elif(curr_state_g in prev_s):
                path = [curr_state_g]
                state_s = curr_state_g
                state_g = curr_state_g
            # reverse to find path for first BFS tree
            while(state_s != root_s):
                state_s = prev_s[state_s]
                path.insert(0, state_s)
            
            # reverse to find the connected path for second BFS tree
            while(state_g != root_g):
                state_g = prev_g[state_g]
                path.append(state_g)

            return path
        addValidChildren(maze, fringe_s, curr_state_s, prev_s, visited_s)
        addValidChildren(maze, fringe_g, curr_state_g, prev_g, visited_g)
    return "No solution"

# -----------A Star-----------
def getEuclid(dim, x, y):
    a = (dim - 1 - x) ** 2
    b = (dim - 1 - y) ** 2
    return numpy.sqrt(a + b)


def getManhattan(dim, x, y):
    a = abs(dim - 1 - x)
    b = abs(dim - 1 - y)
    return a + b


def aStarEuclid(maze):
    dim = maze.size
    visited = {}

    # heuristicList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0)]]
    heuristicList = [[(getEuclid(dim, 0, 0))]]
    while sortedList:
        path = sortedList.pop()
        pathHeuristic = heuristicList.pop()
        # print("Sorted List: ", sortedList)
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


def aStarManhattan(maze):
    dim = maze.size
    visited = {}

    # (x,x,x) represents (x coord, y coord, heuristic)
    # sortedList is sorted from highest to lowest heuristic
    sortedList = [[(0, 0)]]
    heuristicList = [[(getManhattan(dim, 0, 0))]]
    while sortedList:
        path = sortedList.pop()
        pathHeuristic = heuristicList.pop()
        # print("Sorted List: ", sortedList)
        node = path[-1]
        visited[node] = 1
        if maze[node] == 'G':
            return path
        else:
            getNeighborsManhattan(maze, node[0], node[1], visited, sortedList, heuristicList, path, dim)

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


def getNeighborsManhattan(maze, x, y, visited, sortedList, heuristicList, pathO, dim):
    if isValid(maze, x - 1, y) and visited.get((x - 1, y)) is None:
        path1 = pathO.copy()
        path1.append((x - 1, y))
        sortedList.append(path1)
        heuristicList.append(getManhattan(dim, x - 1, y))
    if isValid(maze, x, y - 1) and visited.get((x, y - 1)) is None:
        path2 = pathO.copy()
        path2.append((x, y - 1))
        sortedList.append(path2)
        heuristicList.append(getManhattan(dim, x, y - 1))
    if isValid(maze, x + 1, y) and visited.get((x + 1, y)) is None:
        path3 = pathO.copy()
        path3.append((x + 1, y))
        sortedList.append(path3)
        heuristicList.append(getManhattan(dim, x + 1, y))
    if isValid(maze, x, y + 1) and visited.get((x, y + 1)) is None:
        path4 = pathO.copy()
        path4.append((x, y + 1))
        sortedList.append(path4)
        heuristicList.append(getManhattan(dim, x, y + 1))
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
            print(self[x][y], end="     ")


maze = createMaze(20, 0.2)
printMaze(maze)
print("\nDFS: ")
print(dfs(maze))
print("Length: ", len(dfs(maze)))
print("\nBFS: ")
print(bfs(maze))
print("Length: ", len(bfs(maze)))
print("\nA* Euclidean: ")
print(aStarEuclid(maze))
print("Length: ", len(aStarEuclid(maze)))
print("\nA* Manhattan: ")
print(aStarManhattan(maze))
print("Length: ", len(aStarManhattan(maze)))
print("\nBidirectional: ")
print(bidirectional_bfs(maze))
print("Length: ", len(bidirectional_bfs(maze)))
