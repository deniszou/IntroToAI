import Image
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
    pixelList = {}
    greyColorList = {}
    trueColorList = {}
    repColorList = {}
    greyNeighbors = []
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
            # convert left side to rep colors
            repColorList[x, y] = findClosest(truecolorList[x, y], repColors)
            # convert right side with knn
            for pixel in pixelList[x, y]:
                greyBlock.append(greyColorList[pixel])
            greyNeighbors = findNeighbors(pixelList, greyBlock, greyColorList, width, height, 6)
    for coord in greyNeighbors:
        if


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
        for point in list.values():
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


def eucd(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))


def findClosest(point, list):
    min = (100000, 0)
    for i in range(0, 5):
        if eucd(point, list[i]) < min:
            min = (eucd(point, list[i]), i)
    return list[min[1]]


#knn function
def findNeighbors(blockList, block, list, width, height, n):
    distList = []
    xyList = {}
    res = []
    greyBlock = []
    j = 0
    for x in width/2:
        for y in height:
            for pixel in blockList[x, y]:
                greyBlock.append(list[pixel])
            xyList[eucd(block, greyBlock)] = (x, y)
            distList[j] = eucd(block, greyBlock)
            j += 1
    distList.sort()
    for i in range(0, n):
        res.append(xyList.get(distList[i]))
    return res
