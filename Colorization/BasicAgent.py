from PIL import Image
import numpy
import math

def parsepixels(file):
    im = Image.open(file)
    width, height = im.size
    #k = 0
    rmax = 0
    gmax = 0
    bmax = 0
    pixelList = {}
    greyColorList = {}
    trueColorList = {}
    repColorList = {}
    testColorList = {}
    #tlist = []
    #create list of 3x3
    #create list of rgb, greyscale, repcolor
    #iterate through pixels
    for x in range(0, width):
        #tcol = []
        for y in range(0, height):
            block = []
            #iterate through 3x3 block
            if x != 0 and x != width - 1 and y != 0 and y != height - 1:
                for i in range(-1,2):
                    for j in range(-1,2):
                        block.append((x + i, y + j))
                #pixelList is a list of 3x3 blocks
                pixelList[x, y] = block
            trueColorList[x, y] = im.getpixel((x, y))
            #tcol.append(im.getpixel((x, y)))
            greyColorList[x, y] = trueColorList[x, y][0] * 0.21 + trueColorList[x, y][1] * 0.72 + trueColorList[x, y][2] * 0.07
        #tlist.append(tcol)
            #if trueColorList[k][0] > rmax:
            #    rmax = trueColorList[k][0]
            #if trueColorList[k][1] > gmax:
            #    gmax = trueColorList[k][1]
            #if trueColorList[k][2] > bmax:
            #    bmax = trueColorList[k][2]

            #k += 1
    data = numpy.asarray(im)
    #create grayscale image
    gsList = []
    for x in range(0, height):
        col = []
        for y in range(0, width):
            col.append(int(greyColorList[y,x]))
        gsList.append(col)
    gsArray = numpy.asarray(gsList, dtype = 'uint8')
    print('grey')
    grayImage = Image.fromarray(gsArray, 'L')
    grayImage.save('grey.png')

    #testing data for output
    csList = []
    for x in range(0, height):
        csList.append([])
        for y in range(0, width):
            csList[x].append(trueColorList[y,x])
    csArray = numpy.asarray(csList, dtype = 'uint8')
    print('color')

    colorImage = Image.fromarray(csArray, 'RGB')
    colorImage.save('color.png')

    kmeansRes = kmeans(trueColorList, width, height)
    repColors = kmeansRes[0]
    clusters = kmeansRes[1]
    cDict = kmeansRes[2]

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            # convert to rep colors
            repColorList[x, y] = findClosest(trueColorList[x, y], repColors)

    #output 5color image
    repList = []
    for x in range(1, height - 1):
        col = []
        for y in range(1, width - 1):
            col.append(repColorList[y, x])
        repList.append(col)
    repArray = numpy.asarray(repList, dtype='uint8')
    print('5color')
    repImage = Image.fromarray(repArray, 'RGB')
    repImage.save('5color.png')

    # convert right side with knn
    for x in range(int(width/2), width - 1):
        for y in range(int(height/2), height - 1):
            greyBlock = []
            for pixel in pixelList[x, y]:
                greyBlock.append(greyColorList[pixel])
            testColorList[x, y] = findNeighbors(x, y, cDict, clusters, repColors, repColorList, pixelList, greyBlock, greyColorList, width, height, 6)

    finalOutput = repColorList
    for x in range(int(width/2), width - 1):
        for y in range(int(height/2), height - 1):
            finalOutput[x, y] = testColorList[x, y]

    #final output here
    finalList = []
    for x in range(1, height - 1):
        col = []
        for y in range(1, width - 1):
            col.append(finalList[y, x])
        finalList.append(col)
    finalArray = numpy.asarray(finalList, dtype='uint8')
    print('final')
    finalImage = Image.fromarray(finalArray, 'RGB')
    finalImage.save('final.png')

#run k = 5 clustering here
def kmeans(list, width, height):

    #pick center indices with k = 5
    c = [(numpy.random.randint(0, width),numpy.random.randint(1, height)),
         (numpy.random.randint(0, width),numpy.random.randint(1, height)),
         (numpy.random.randint(0, width),numpy.random.randint(1, height)),
         (numpy.random.randint(0, width),numpy.random.randint(1, height)),
         (numpy.random.randint(0, width),numpy.random.randint(1, height))]

    for i in range(1000):
        # create partitions(group clusters)
        output = [[],[],[],[],[]]  #clusters
        #ind = 0  #shud have looped over range instead
        check = 0  #breaks when centroids repeat
        res = [[],[],[],[],[]]
        clusterDict = {}
        xyClusters = [[],[],[],[],[]]

        for x in range(0, width):
            for y in range(0, height):
                point = list[x, y]
                ind = 0
                mindist = (1000000, 0)
                for centerInd in c:
                    if point == list[centerInd[0], centerInd[1]]:
                        continue
                    distance = eucd(point, list[centerInd[0], centerInd[1]])
                    # print(distance)
                    if distance < mindist[0]:
                        mindist = (distance, ind)
                    ind += 1
                    # print(ind)
                # print(mindist)
                output[mindist[1]].append(point)
                xyClusters[mindist[1]].append((x, y))
                clusterDict[x, y] = mindist[1]
        #print(mindist)
        #calculate true mean for each cluster
        for j in range(0, 5):
            meanArr = numpy.mean(output[j], axis=0)
            mean = tuple(map(int,meanArr.tolist()))
            if list[c[j]] == mean:
                res[j] = list[c[j]]
                check += 1
            list[c[j]] = mean
        if check == 5:
            return res, xyClusters, clusterDict
            break
    return res, xyClusters, clusterDict

def eucd(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))


def findClosest(point, list):
    min = (100000, 0)
    for i in range(0, 5):
        if eucd(point, list[i]) < min[0]:
            min = (eucd(point, list[i]), i)
    return list[min[1]]


#knn function greyblock holds grey values for 3x3 blocks on training side, compared against block, returns list of middle pixels
def findNeighbors(ex, why, cDict, clusters, repColors, repColorsList, blockList, block, alist, width, height, n):
    distList = []
    coords = []
    maxList = []
    colorCount = [0, 0, 0, 0, 0]
    max = 0

    for point in clusters[cDict[ex, why]]:
        x = point[0]
        y = point[1]
        if x > 1 and x < width/2 and y > 1 and y < height - 1:
            greyBlock = []
            for pixel in blockList[x, y]:
                greyBlock.append(alist[pixel])
            #xyList[eucd(block, greyBlock)] = (x, y)
            distList.append((eucd(block, greyBlock), (x, y)))
            #else:
            #    distList[j] = (eucd(block, greyBlock), (x, y))
            #j += 1
    distList.sort(key = lambda dist: dist[0])

    for i in range(0, n):
        coords.append(distList[i])
    for coord in coords:
        for color in repColors:
            if repColorsList[coord[1]] == color:
                lcoord = list(coord)
                lcoord.append(repColors.index(color))
                coords[coords.index(coord)] = lcoord
                colorCount[repColors.index(color)] += 1
    for num in colorCount:
        if num > max:
            max = num
    for count in colorCount:
        if count == max:
            maxList.append(colorCount.index(count))
            colorCount[colorCount.index(count)] = 0
    if len(maxList) == 1:
        return repColors[maxList[0]]
    else:
        for coord in coords:
            for m in maxList:
                if m == coord[2]:
                    return repColors[m]
    return "error"


parsepixels('beach.png')