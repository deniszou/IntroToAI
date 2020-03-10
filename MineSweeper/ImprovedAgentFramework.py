# bfs through the board generating probabilities, if end is reached open lowest
def iterateBoard(board, dim)
    queue = [(0, 0)]
    minProb = 1
    visited = {}

    while queue:
        cell = queue.pop(0)
        visited[cell] = 1

        # generating boards is expensive so only do so if there are clueNeighbors
        # optionally make it so it only checks if prob > 0 and skip if prob is 0
        if checkNeighbors(board, cell[0], cell[1]):
            prob = generateBoards(board, cell[0], cell[1])
            if prob == 0:
            # open this one and restart
            elif prob < minProb:
                minProb = prob

        if board[cell] == board[dim - 1, dim - 1]:
        # here open lowest probability
        else:
            getNeighbors(board, cell[0], cell[1], queue, visited)

    return board


def getNeighbors(board, x, y, queue, visited):
    if isValid(board, x - 1, y) and visited.get((x - 1, y)) is None:
        # down
        queue.append((x - 1, y))
    if isValid(board, x - 1, y - 1) and visited.get((x - 1, y - 1)) is None:
        # downleft
        queue.append((x - 1, y - 1))
    if isValid(board, x, y - 1) and visited.get((x, y - 1)) is None:
        # left
        queue.append((x, y - 1))
    if isValid(board, x + 1, y - 1) and visited.get((x + 1, y - 1)) is None:
        # upleft
        queue.append((x + 1, y - 1))
    if isValid(board, x + 1, y) and visited.get((x + 1, y)) is None:
        # up
        queue.append((x + 1, y))
    if isValid(board, x + 1, y + 1) and visited.get((x + 1, y + 1)) is None:
        # upright
        queue.append((x + 1, y + 1))
    if isValid(board, x, y + 1) and visited.get((x, y + 1)) is None:
        # right
        queue.append((x, y + 1))

    return queue


# checks neighbors to see if clueless
def checkNeighbors(board, x, y, queue):
    clueNeighbors = 0
    numNeighbors = 0

    if isValid(board, x - 1, y):
        # down
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x - 1, y - 1):
        # downleft
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x, y - 1):
        # left
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x + 1, y - 1):
        # upleft
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x + 1, y):
        # up
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x + 1, y + 1):
        # upright
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1
    if isValid(board, x, y + 1):
        # right
        if isClue:
            clueNeighbors += 1
        numNeighbors += 1

    if numNeighbors == clueNeighbors:
        return False
    return True


def isValid(board, x, y):
    if x < 0 or y < 0 or (x > board.shape[0] - 1) or y > (board.shape[1] - 1):
        return False
    return True


def generateBoards(board, x, y):


