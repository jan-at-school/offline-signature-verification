
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
import os


class FeatureExtractor:

    sig = None
    path = None
    mime = None

    image = None
    draw = None
    binarizedImage = None

    centroids = np.zeros((64, 2), np.int)
    ratios = np.zeros((64, 1), np.float)
    transitions = np.zeros((64, 1), np.int)

    currBox = 0

    def __init__(self, path, sig, mime):
        self.sig = sig
        self.path = path
        self.mime = mime
        self.image = Image.open(path+'/'+sig+mime)
        # convert to singal channeled image
        self.binarizedImage = self.image.convert("L")
        self.binarizedImage = self.binarizedImage.point(
            lambda x: 0 if x < 150 else 255, '1')  # binarized image
        # self.draw = ImageDraw.Draw(self.image)

    def extract(self):
        mainBox = methods.boundaries(self.binarizedImage)
        self.split(self.binarizedImage, mainBox)

        if not os.path.exists('processed/centroids'):
            os.makedirs('processed/centroids')

        if not os.path.exists('processed/transitions'):
            os.makedirs('processed/transitions')

        if not os.path.exists('processed/ratios'):
            os.makedirs('processed/ratios')

        print(self.centroids)
        np.savetxt('processed/centroids/'+self.sig+'.txt', self.centroids,fmt = '%d')
        np.savetxt('processed/transitions/'+self.sig+'.txt', self.transitions)
        np.savetxt('processed/ratios/'+self.sig+'.txt', self.ratios)

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

            self.centroids[self.currBox][0] = cx
            self.centroids[self.currBox][1] = cy
            self.transitions[self.currBox][0] = t
            self.ratios[self.currBox][0] = r
            self.currBox += 1
            # self.centroids = np.append(self.centroids, [(cx, cy)])
            # self.transitions = np.append(self.transitions, [t])
            # self.ratios = np.append(self.ratios, [r])

            # self.draw.rectangle(((thisBox.left, thisBox.top),
            #                      (thisBox.right, thisBox.bottom)), outline="yellow")

    def findRatio(self, box):
        return (box.right-box.left)*1.00/(box.bottom-box.top)
