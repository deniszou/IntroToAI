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
    trueColorList = []
    #create list of 3x3
    #create list of rgb
    #iterate through pixels
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            #iterate through 3x3 block
            for i in range(-1,2):
                for j in range(-1,2):
                    block.append(x + i, y + j)
            pixelList[x, y] = block
            trueColorList[k] = im.getpixel(x,y)
            if trueColorList[k][0] > rmax:
                rmax = trueColorList[k][0]
            if trueColorList[k][1] > gmax:
                gmax = trueColorList[k][1]
            if trueColorList[k][2] > bmax:
                bmax = trueColorList[k][2]
            k += 1
    repColors = kmeans(trueColorList, k)


#run k = 5 clustering here
def kmeans(list, listSize):

    #pick center indices with k = 5
    c = np.random.randint(0, listSize, size=5)

    for i in range(1000):
        # create partitions(group clusters)
        output = []  #clusters
        ind = 0  #shud have looped over range instead
        check = 0  #breaks when centroids repeat
        mindist = (1000000, 0)
        for point in list:
            for center in c:
                if point == center:
                    continue
                distance = eucd(point, center)
                if distance < mindist[0]:
                    mindist = (distance, ind)
                ind += 1
            output[mindist[1]].append(point)

        #calculate true mean for each cluster
        for i in range(0, 5):
            mean = numpy.mean(output[i], axis=1)
            if c[i] == mean:
                check += 1
            c[i] = mean
        if check == 4:
            return c
            break


def eucd(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))