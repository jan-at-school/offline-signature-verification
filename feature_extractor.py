
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
import os


class FeatureExtractor:

    sig = 'R0001'
    path = 'res'
    mime = '.png'

    image = None
    draw = None
    binarizedImage = None

    centroids = np.zeros((0, 2), np.int)
    ratios = np.zeros((0, 1), np.int)
    transitions = np.zeros((0, 1), np.int)

    def __init__(self, path, sig, mime):
        self.sig = sig
        self.path = path
        self.mime = mime
        self.image = Image.open(path+'/'+sig+mime)
        # convert to singal channeled image
        self.binarizedImage = self.image.convert("L")
        self.binarizedImage = self.binarizedImage.point(
            lambda x: 0 if x < 150 else 255, '1')  # binarized image
        self.draw = ImageDraw.Draw(self.image)

    def extract(self):
        mainBox = methods.boundaries(self.binarizedImage)
        self.split(self.binarizedImage, mainBox)

    def split(self, image, thisBox, depth=0):
        cx, cy = methods.centroid(self.binarizedImage, thisBox)
        if depth < 3:
            self.split(image, BOX(thisBox.left, cx,
                                  thisBox.top, cy), depth + 1)
            self.split(image, BOX(cx, thisBox.right,
                                  thisBox.top, cy), depth + 1)
            self.split(image, BOX(thisBox.left,
                                  cx, cy, thisBox.bottom), depth + 1)
            self.split(image, BOX(cx, thisBox.right,
                                  cy, thisBox.bottom), depth + 1)

        else:
            t = methods.transitions(image, thisBox)
            r = self.findRatio(thisBox)

            self.centroids = np.append(self.centroids, [[cx, cy]])
            self.transitions = np.append(self.transitions, [t])
            self.ratios = np.append(self.ratios, [r])
            print(t, r)

            self.draw.rectangle(((thisBox.left, thisBox.top),
                                 (thisBox.right, thisBox.bottom)), outline="yellow")

    def findRatio(self, box):
        return (box.right-box.left)*1.00/(box.bottom-box.top)
