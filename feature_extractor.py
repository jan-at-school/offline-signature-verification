
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
from math import atan
import os
import math


class FeatureExtractor:

    sig = None
    path = None
    mime = None

    image = None
    draw = None
    binarizedImage = None

    boxes = list()

    centroids = np.zeros((64, 2), np.int)
    ratios = np.zeros((64, 1), np.float)
    transitions = np.zeros((64, 1), np.int)
    angles = np.zeros((64, 1), np.float)
    blacks = np.zeros((64, 1), np.int)

    normalizedSize = np.zeros((64, 1), np.float)
    normalizedSumOfAngles = np.zeros((64, 1), np.float)

    currBox = 0

    config = {
        'threshold': 200
    }

    def __init__(self, filePath, sig, mime, config=None):

        self.config = config if not config == None else self.config
        self.sig = sig

        self.path = os.path.dirname(filePath)
        filename, file_extension = os.path.splitext(filePath)
        self.mime = file_extension
        self.image = Image.open(filePath)
        # convert to singal channeled image
        self.binarizedImage = self.image.convert("L")
        self.binarizedImage = self.binarizedImage.point(
            lambda x: 0 if x < self.config.get('threshold') else 255, '1')  # binarized image
        self.draw = ImageDraw.Draw(self.binarizedImage)

    def extract(self):
        mainBox = methods.boundaries(self.binarizedImage)
        self.split(self.binarizedImage, mainBox)

        if not os.path.exists('processed/centroids'):
            os.makedirs('processed/centroids')
        if not os.path.exists('processed/transitions'):
            os.makedirs('processed/transitions')
        if not os.path.exists('processed/ratios'):
            os.makedirs('processed/ratios')
        if not os.path.exists('processed/angles'):
            os.makedirs('processed/angles')
        if not os.path.exists('processed/blacks'):
            os.makedirs('processed/blacks')
        if not os.path.exists('processed/normalizedSize'):
            os.makedirs('processed/normalizedSize')
        if not os.path.exists('processed/normalizedSumOfAngles'):
            os.makedirs('processed/normalizedSumOfAngles')

        np.savetxt('processed/centroids/'+self.sig +
                   '.txt', self.centroids, fmt='%d')
        np.savetxt('processed/transitions/'+self.sig+'.txt', self.transitions)
        np.savetxt('processed/ratios/'+self.sig+'.txt', self.ratios)
        np.savetxt('processed/angles/'+self.sig+'.txt', self.angles)
        np.savetxt('processed/blacks/'+self.sig+'.txt', self.blacks, fmt='%d')
        np.savetxt('processed/normalizedSize/' +
                   self.sig+'.txt', self.normalizedSize)
        np.savetxt('processed/normalizedSumOfAngles/' +
                   self.sig+'.txt', self.normalizedSumOfAngles)

        # self.binarizedImage.show()

    '''
    Recursive function to split the image into 64 cells
    '''

    def split(self, image, thisBox, depth=0):
        cx, cy = methods.centroid(image, thisBox)

        if depth < 3:
            self.split(image, BOX(thisBox.left, cx,
                                  thisBox.top, cy), depth + 1)
            self.split(image, BOX(cx, thisBox.right,
                                  thisBox.top, cy), depth + 1)
            self.split(image, BOX(thisBox.left,
                                  cx, cy, thisBox.bottom), depth + 1)
            self.split(image, BOX(cx, thisBox.right,
                                  cy, thisBox.bottom), depth + 1)

        else:  # completely divided
            # if the box is completely divided add it to the list
            try:
                self.saveFeatures(image, thisBox, (cx, cy), self.currBox)
            except Exception as e:
                self.binarizedImage.show()

            self.currBox += 1
            self.draw.rectangle(((thisBox.left, thisBox.top),
                                 (thisBox.right, thisBox.bottom)), outline="black")

    def saveFeatures(self, image, thisBox, centroid, boxNo):
        transitions, blacks, blackAngleSum = methods.blackFeatures(
            image, thisBox)
        # print(transitions,blacks,blackAngleSum,float(blacks)/float(thisBox.getTotalPixels()))
        zeroBox = thisBox.isZeroBox()

        self.boxes.append(thisBox)
        self.centroids[boxNo][0], self.centroids[boxNo][1] = centroid
        self.transitions[boxNo][0] = transitions
        self.blacks[boxNo][0] = blacks
        self.angles[boxNo][0] = self.angle(centroid, thisBox)

        if zeroBox:
            self.binarizedImage.show()
            self.ratios[boxNo][0] = 0
            self.normalizedSize[boxNo][0] = 0.5
        else:
            self.normalizedSize[boxNo][0] = float(
                blacks)/float(thisBox.getTotalPixels())
            self.ratios[boxNo][0] = thisBox.getAspectRatio()

        self.normalizedSumOfAngles[boxNo][0] = blackAngleSum

    def angle(self, centroid, thisBox):
        p1 = centroid
        p2 = thisBox.right, thisBox.bottom
        return math.atan2(p1[1]-p2[1], p1[0] - p2[0])
