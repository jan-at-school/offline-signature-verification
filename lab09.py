
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


questionFilesPath = storage.DATASET_PATH + '/TestSet/Questioned'
refFilesPath = storage.DATASET_PATH + '/TestSet/Reference'
# inputFiles = os.listdir(resFilePath)
# totalSigs = len(os.listdir('processed/centroids'))

refSigNo = 2
refSig = refFilesPath+'/R{:03d}.png'.format(
    refSigNo)


refResult = feature_extractor.FeatureExtractor(
    refSig, refSigNo).extract()

pp(refResult)


print(storage.getDataSetCount())
processedData = storage.getAllProcessed()



distBlacks = list()
distAngles = list()
distNormalizedSize = list()
distNormalizedSumOfAngles = list()
distRatios = list()
distTransitions = list()
distCentroids = list()



# pp(processedData) # print
distAggregate = dict()
distList = dict()
sigNames = list()
colors = list()
for sigFeature in processedData:
    
    
    
    distBlacks = methods.eclideanDist(sigFeature.blacks, refResult.blacks)
    distAngles = methods.eclideanDist(sigFeature.angles, refResult.angles)
    distNormalizedSize = methods.eclideanDist(sigFeature.normalizedSize, refResult.normalizedSize)
    distNormalizedSumOfAngles = methods.eclideanDist(sigFeature.normalizedSumOfAngles,refResult.normalizedSumOfAngles)
    distRatios = methods.eclideanDist(sigFeature.ratios, refResult.ratios)
    distTransitions = methods.eclideanDist(sigFeature.transitions, refResult.transitions)
    distCentroids = methods.eclideanDistForCentroids(sigFeature.centroids, refResult.centroids)



    sigNames.append(sigFeature.sigNo)
    
    
    

    

    distList['D{:02d}{:02d}'.format(refSigNo, sigFeature.sigNo)] = {
        'distBlacks': distBlacks,
        'distAngles': distAngles,
        'distNormalizedSize': distNormalizedSize,
        'distNormalizedSumOfAngles': distNormalizedSumOfAngles,
        'distRatios': distRatios,
        'distTransitions': distTransitions,
        'distCentroids': distCentroids

    }
    distAggregate['D{:02d}{:02d}'.format(refSigNo, sigFeature.sigNo)] = distAngles +\
        distRatios + \
        distTransitions +\
        distNormalizedSize +\
        distNormalizedSumOfAngles +\
        distCentroids

    pp(distList)


featureVectors = {
    'f1':distAngles,
    'f2':distNormalizedSize,
    'f3':distNormalizedSumOfAngles,
    'f4':distRatios,
    'f5':distCentroids,
    'f6':distBlacks,
    'f7':distTransitions
}


