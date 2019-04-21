
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
from math import atan
import os
import math
import feature_extractor
import storage
from beeprint import pp
import matplotlib.pylab as plt

# class KNNTest:


resFilePath = 'res'
inputFiles = os.listdir(resFilePath)
totalSigs = len(os.listdir('processed/centroids'))

questionedSig = 'dataset/test/forgeries_{person}_{signNo}.png'.format(
    person=9, signNo=24)


refResult = feature_extractor.FeatureExtractor(
    questionedSig, None, None, None).extract()

print(refResult.angles)


print(storage.getDataSetCount())
processedData = storage.getAllProcessed()
# pp(processedData) # print
distList = dict()
distAggregate = dict()
for sigFeature in processedData:
    distBlacks = methods.eclideanDist(sigFeature.blacks, refResult.blacks)
    distAngles = methods.eclideanDist(sigFeature.angles, refResult.angles)
    distNormalizedSize = methods.eclideanDist(
        sigFeature.normalizedSize, refResult.normalizedSize)
    distNormalizedSumOfAngles = methods.eclideanDist(sigFeature.normalizedSumOfAngles,
                                                     refResult.normalizedSumOfAngles)
    distRatios = methods.eclideanDist(sigFeature.ratios, refResult.ratios)
    distTransitions = methods.eclideanDist(
        sigFeature.transitions, refResult.transitions)
    distCentroids = methods.eclideanDistForCentroids(
        sigFeature.centroids, refResult.centroids)

    distList['{:d}_{:02d}'.format(int(sigFeature.groupNo), int(sigFeature.sigNo))] = {
        'distBacks': distBlacks,
        'distAngles': distAngles,
        'distNormalizedSize': distNormalizedSize,
        'distNormalizedSumOfAngles': distNormalizedSumOfAngles,
        'distRatios': distRatios,
        'distTransitions': distTransitions,
        'distCentroids': distCentroids

    }
    

pp(distList)

lists = sorted(distAggregate.items())  # sorted by key, return a list of tuples

x, y = zip(*lists)  # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.show()
