
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
from math import atan
import os
import math
import storage
from threading import Thread
from multiprocessing import Process, Lock
from beeprint import pp


mutex = Lock()


class FeatureExtractorThread(Thread):

    featureExtractor = None
    sigNo = None
    totalSigs = None

    def __init__(self, filePath, sigNo, totalSigs, config=None):
        ''' Constructor. '''
        Thread.__init__(self)
        self.filePath = filePath
        self.config = config
        self.sigNo = sigNo
        self.totalSigs = totalSigs
        

    def run(self):
        self.featureExtractor = FeatureExtractor(
            self.filePath, self.sigNo, self.config)
        print(self.sigNo, 'out if', self.totalSigs)
        self.featureExtractor.extractAndSave()
        


class SigFeatures:


    sigNo = None

    centroids = np.zeros((64, 2), np.int)
    ratios = np.zeros(64, np.float)
    transitions = np.zeros(64, np.int)
    angles = np.zeros(64, np.float)
    blacks = np.zeros(64, np.int)
    normalizedSize = np.zeros(64, np.float)
    normalizedSumOfAngles = np.zeros(64, np.float)


    def __init__(self,sigNo):
        self.sigNo = sigNo
        self.centroids = self.centroids
        



class FeatureExtractor:


    sigNo = None
    overAllSigNo = None
    path = None
    mime = None


    filePath = None
    image = None
    draw = None
    binarizedImage = None

    boxes = list()


    sigFeatures = None
    

    currBox = 0

    config = {
        'threshold': 188,
        'outputPath': 'processed'
    }

    def __init__(self, filePath, sigNo, config=None):

        self.config = config if not config == None else self.config
        self.sigNo = sigNo
        self.overAllSigNo = sigNo
        self.sigFeatures = SigFeatures(sigNo)
        self.filePath = filePath
        self.path = os.path.dirname(filePath)
        filename, file_extension = os.path.splitext(filePath)
        self.mime = file_extension
        self.image = Image.open(filePath)
        # half = 0.5
        # self.image = self.image.resize(
        #     [int(half * s) for s in self.image.size])
        # convert to singal channeled image
        self.binarizedImage = self.image.convert("L")
        threshold = self.config.get('threshold')


        self.binarizedImage = self.binarizedImage.point(
            lambda x: 0 if x < threshold else 255, '1')  # binarized image
        self.draw = ImageDraw.Draw(self.binarizedImage)


    def extractAndSave(self):
        self.extract()

        storage.store(self.config.get('outputPath'),self.sigNo, self.sigFeatures)

        print('Completed                                           ', self.sigNo)
        # self.binarizedImage.show()

    def extract(self):
        
        mainBox = methods.boundaries(self.binarizedImage)
        
        self.draw.rectangle(((mainBox.left, mainBox.top),
                             (mainBox.right, mainBox.bottom)), outline="black")
        self.split(self.binarizedImage, mainBox)
        
        print('Completed                                           ', self.sigNo)
        return self.sigFeatures

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
                print(e)
            
            self.currBox += 1
            self.draw.rectangle(((thisBox.left, thisBox.top),
                                 (thisBox.right, thisBox.bottom)), outline="black")

    def saveFeatures(self, image, thisBox, centroid, boxNo):
        transitions, blacks, blackAngleSum = methods.blackFeatures(
            image, thisBox)
        # print(transitions,blacks,blackAngleSum,float(blacks)/float(thisBox.getTotalPixels()))
        zeroBox = thisBox.isZeroBox()

        self.boxes.append(thisBox)
        self.sigFeatures.centroids[boxNo][0], self.sigFeatures.centroids[boxNo][1] = centroid
        self.sigFeatures.transitions[boxNo] = transitions
        self.sigFeatures.blacks[boxNo] = blacks
        self.sigFeatures.angles[boxNo] = self.angle(centroid, thisBox)

        if zeroBox:
            # self.binarizedImage.show()
            self.sigFeatures.ratios[boxNo] = 0
            self.sigFeatures.normalizedSize[boxNo] = 0.5
        else:
            self.sigFeatures.normalizedSize[boxNo] = float(
                blacks)/float(thisBox.getTotalPixels())
            self.sigFeatures.ratios[boxNo] = thisBox.getAspectRatio()

        self.sigFeatures.normalizedSumOfAngles[boxNo] = blackAngleSum

    def angle(self, centroid, thisBox):
        p1 = centroid
        p2 = thisBox.right, thisBox.bottom
        return math.atan2(p1[1]-p2[1], p1[0] - p2[0])

    