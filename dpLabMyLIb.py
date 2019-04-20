import itertools
import PIL
from PIL import Image
import numpy as np
import itertools
import sys
from threading import Thread
from multiprocessing import Process, Lock


class BOX:
    left = None
    bottom = None
    top = None
    right = None

    size = None

    def __init__(self, left, top, right, bottom):
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right
        self.size = (self.right-self.left,
                     self.bottom-self.top)

    def __str__(self):
        return " <BOX left:%d top:%d right:%d bottom:%d> " % (self.left, self.top, self.right, self.bottom)


def equalizeHistogram(image, pixels, box):
    width, height = box.size
    totalPixels = width * height

    freq = [0] * 256  # fill
    cProbability = [0] * 256  # fill zeros

    for x, y in itertools.product(range(box.left, box.left + width), range(box.top, box.top+height)):
        freq[pixels[x, y]] += 1

    # HISTOGRAM EQUALIZATION
    prevSum = 0
    for i in range(256):
        prevSum += freq[i]*1.0/totalPixels  # add the probablity to calculate
        cProbability[i] = prevSum

    for x, y in itertools.product(range(box.left, box.left + width), range(box.top, box.top+height)):
        # (L-1) * cummulative probability
        pixels[x, y] = int((255 * cProbability[pixels[x, y]]))

    return image

mutex = Lock()
class EqualizeWindowThread(Thread):

    def __init__(self, image, pixels, box):
        ''' Constructor. '''
        Thread.__init__(self)
        self.image = image
        self.pixels = pixels
        self.box = box

    def run(self):
        image = self.image
        pixels = self.pixels 
        box = self.box
        width, height = box.size
        totalPixels = width * height

        freq = [0] * 256  # fill
        cProbability = [0] * 256  # fill zeros

        for x, y in itertools.product(range(box.left, box.left + width), range(box.top, box.top+height)):
            freq[image.getpixel((x, y))] += 1

        # HISTOGRAM EQUALIZATION
        prevSum = 0
        for i in range(256):
            prevSum += freq[i]*1.0/totalPixels  # add the probablity to calculate
            cProbability[i] = prevSum
        with mutex:
            for x, y in itertools.product(range(box.left, box.left + width), range(box.top, box.top+height)):
                # (L-1) * cummulative probability
                pixels[x, y] = int((255 * cProbability[image.getpixel((x, y))]))

        print('Thread completed its work' + str(box))