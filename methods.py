import itertools
import math



class BOX:
    left = None
    bottom = None
    top = None
    right = None

    def __init__(self, left, right, top, bottom):
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right

    def getSize(self):
        return (int(self.right-self.left),
                     int(self.bottom-self.top))
    def getTotalPixels(self):
        return ((self.right-self.left)*
                     (self.bottom-self.top))

    def getAspectRatio(self):
        return float(self.right -self.left)/float(self.bottom - self.top)
    def isZeroBox(self):
        return (self.right -self.left) == 0 or (self.bottom - self.top) == 0
    '''
    
    Returns the total number of pixels
    '''

    def getTotalCount(self):
        width, height = self.getSize()
        return int(width * height)

    def __str__(self):
        return "<BOX left:%d bottom:%d top:%d right:%d>" % (self.left, self.bottom, self.top, self.right)


def centroid(image, box):
    width, height = (abs(box.right-box.left),
                     abs(box.bottom-box.top))
    cx = int(0)
    cy = int(0)
    n = 1
    for x, y in itertools.product(range(width), range(height)):
        if image.getpixel((box.left+x, box.top+y)) == 0:
            cx = cx + x
            cy = cy + y
            n = n + 1

    
    cx = box.left+ int(cx / n)
    cy = box.top+ int(cy / n)
    
    return (cx, cy)

def blackFeatures(image, box):
    width, height = (box.right-box.left,
                     box.bottom-box.top)
    prev = image.getpixel((0, 0))
    n = 0
    blacks = 0
    blackAngleSum = 0
    for x, y in itertools.product(range(width), range(height)):
        curr = image.getpixel((box.left + x, box.top + y))
        if curr == 255 and prev == 0:
            n = n + 1
        prev = curr

        if curr == 0:
            blacks += 1
            if(x == box.left):
                    blackAngleSum += math.pi / 2
            else:
                blackAngleSum += math.atan((float)(box.bottom-y) / (float)(x-box.left))
        
    return (n,blacks,blackAngleSum)




def boundaries(binarizedImage):

    width, height = binarizedImage.size
    leftt = width
    rightt = 0
    topp = height
    bottomm = 0
    for x, y in itertools.product(range(width), range(height)):
        color = binarizedImage.getpixel((x, y))

        if color == 0:
            if x > rightt:
                rightt = x
            if x < leftt:
                leftt = x
            if y > bottomm:
                bottomm = y
            if y < topp:
                topp = y
    return BOX(leftt, rightt, topp, bottomm)






def eclideanDist(array1,array2):
    summ = 0 
    for i in range(len(array1)):
        summ += math.pow(array2[i] - array1[1],2)

    return math.sqrt(summ)



def eclideanDistForCentroids(array1,array2):
    summ = 0 
    for i in range(len(array1)):
        cx = array1[i][0]
        cy = array1[i][1]

        refMagnitude = math.sqrt(cx*cx + cy*cy)

        tcx = array2[i][0]
        tcy = array2[i][1]    
        testMagnitude = math.sqrt(tcx*tcx + tcy*tcy)


        summ += math.pow((testMagnitude - refMagnitude),2)

    return math.sqrt(summ)
