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
        return (self.right-self.left,
                     self.bottom-self.top)
    '''
    Returns the total number of pixels
    '''
    def getTotalCount(self):
        width,height = self.getSize()
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
    cx = box.left+ cx / n
    cy = box.top+ cy / n
    return (cx, cy)


def transitions(image, box):
    width, height = (box.right-box.left,
                     box.bottom-box.top)
    prev = image.getpixel((0, 0))
    n = 0
    for x, y in itertools.product(range(width), range(height)):
        curr = image.getpixel((box.left + x, box.top + y))
        if curr == 255 and prev == 0:
            n = n + 1
        prev = curr
    return n




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


def blackCount(image, box):
    width, height = box.getSize()
    n = 0
    for x, y in itertools.product(range(width), range(height)):
        curr = image.getpixel((box.left + x, box.top + y))
        if curr == 0:
            n = n + 1
    return n
