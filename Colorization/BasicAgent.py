import Image
import numpy

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
    for x in range(1, width - 1):
        for y in range(1, height - 1):
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
    repColors = kmeans(trueColorList, rmax, gmax, bmax, k)


#run k = 5 clustering here
def kmeans(list, rmax, gmax, bmax, listSize):

    #pick center indices
    c = np.random.randint(0, listSize, size=5)
    
