import PIL
from PIL import Image
import numpy
import math

def parsepixels(file):
    im = Image.open(file)
    width, height = im.size
    block = []
    k = 0
    rmax = 0
    gmax = 0
    bmax = 0
    pixelList = []
    greyColorList = []
    trueColorList = []
    repColorList = []
    testColorList = []
    #greyNeighbors = []
    greyBlock = []
    #create list of 3x3
    #create list of rgb, greyscale, repcolor
    #iterate through pixels
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            #iterate through 3x3 block
            for i in range(-1,2):
                for j in range(-1,2):
                    block.append(x + i, y + j)
            #pixelList is a list of 3x3 blocks
            pixelList[x, y] = block
            trueColorList[x, y] = im.getpixel(x,y)
            greyColorList[x, y] = trueColorList[x, y][0] * 0.21 + trueColorList[x, y][1] * 0.72 + trueColorList[x, y][2] * 0.07

            #if trueColorList[k][0] > rmax:
            #    rmax = trueColorList[k][0]
            #if trueColorList[k][1] > gmax:
            #    gmax = trueColorList[k][1]
            #if trueColorList[k][2] > bmax:
            #    bmax = trueColorList[k][2]

            k += 1
    repColors = kmeans(trueColorList, width, height)

    for x in range(0, width):
        for y in range(0, height):
            # convert to rep colors
            repColorList[x, y] = findClosest(truecolorList[x, y], repColors)

    # convert right side with knn
    for x in range(width/2, width):
        for y in range(height/2, height):
            for pixel in pixelList[x, y]:
                greyBlock.append(greyColorList[pixel])
            testColorList[x, y] = findNeighbors(repColors, repColorsList, pixelList, greyBlock, greyColorList, width, height, 6)

    finalOutput = repColorList
    for x in range(width/2, width):
        for y in range(height/2, height):
            finalOutput[x, y] = testColorList[x, y]

    grayImage = Image.fromarray(greyColorList)
    img.save('grey.png')
    fiveColorImage = Image.fromarray(repColorList)
    img.save('fiveColor.png')
    finalImage = Image.fromarray(finalOutput)
    img.save('trainTest.png')

            #run k = 5 clustering here
def kmeans(list, width, height):

    #pick center indices with k = 5
    c = numpy.random.randint(0, width, size=(5, 2))

    for i in range(1000):
        # create partitions(group clusters)
        output = []  #clusters
        ind = 0  #shud have looped over range instead
        check = 0  #breaks when centroids repeat
        res = []
        mindist = (1000000, 0)
        for point in list:
            for centerInd in c:
                if point == list[centerInd]:
                    continue
                distance = eucd(point, list[centerInd])
                if distance < mindist[0]:
                    mindist = (distance, ind)
                ind += 1
            output[mindist[1]].append(point)

        #calculate true mean for each cluster
        for i in range(0, 5):
            mean = numpy.mean(output[i], axis=1)
            if list[c[i]] == mean:
                res[i] = list[c[i]]
                check += 1
            list[c[i]] = mean
        if check == 4:
            return res
            break
    return res

def eucd(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))


def findClosest(point, list):
    min = (100000, 0)
    for i in range(0, 5):
        if eucd(point, list[i]) < min:
            min = (eucd(point, list[i]), i)
    return list[min[1]]


#knn function greyblock holds grey values for 3x3 blocks on training side, compared against block, returns list of middle pixels
def findNeighbors(repColors, repColorsList, blockList, block, list, width, height, n):
    distList = []
    xyList = {}
    coords = []
    greyBlock = []
    maxList = {}
    eucList = []
    colorCount = [0, 0, 0, 0, 0]
    j = 0

    for x in width/2:
        for y in height:
            for pixel in blockList[x, y]:
                greyBlock.append(list[pixel])
            #xyList[eucd(block, greyBlock)] = (x, y)
            distList[j] = (eucd(block, greyBlock), (x, y))
            j += 1
    distList.sort(distList, key = lambda dist: dist[0])

    for i in range(0, n):
        coords.append(distList[i])
    for coord in coords:
        for color in repColors:
            if repColorsList[coord[1]] == color:
                coord.append(repColors.index(color))
                colorCount[repColors.index(color)] += 1
    for count in colorCount:
        if count == max(colorCount):
            maxList.append(colorCount.index(count))
    if len(maxList) == 1:
        return repColors[maxList[0]]
    else:
        for coord in coords:
            for max in maxList:
                if max == coord[2]:
                    return repColors[max]
    return "error"


parsepixels('beach.png')