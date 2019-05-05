
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

sigNames = list()
colors = list()
for sigFeature in processedData:
#     distBlacks = np.mean(methods.onetoonedist(sigFeature.blacks, refResult.blacks))
#     distAngles = np.mean(methods.onetoonedist(sigFeature.angles, refResult.angles))
#     distNormalizedSize = np.mean(methods.onetoonedist(sigFeature.normalizedSize, refResult.normalizedSize))
#     distNormalizedSumOfAngles = np.mean(methods.onetoonedist(sigFeature.normalizedSumOfAngles,refResult.normalizedSumOfAngles))
#     distRatios = np.mean(methods.onetoonedist(sigFeature.ratios, refResult.ratios))
#     distTransitions = np.mean(methods.onetoonedist(sigFeature.transitions, refResult.transitions))
#     distCentroids = np.mean(methods.onetoonedist(sigFeature.centroids, refResult.centroids),axis=0)

    # distBlacks = np.mean(methods.onetoonedist(refResult.blacks, sigFeature.blacks))
    # distAngles = np.mean(methods.onetoonedist(refResult.angles, sigFeature.angles))
    # distNormalizedSize = np.mean(methods.onetoonedist(refResult.normalizedSize, sigFeature.normalizedSize))
    # distNormalizedSumOfAngles = np.mean(methods.onetoonedist(refResult.normalizedSumOfAngles,sigFeature.normalizedSumOfAngles))
    # distRatios = np.mean(methods.onetoonedist(refResult.ratios, sigFeature.ratios))
    # distTransitions = np.mean(methods.onetoonedist(refResult.transitions, sigFeature.transitions))
    # distCentroids = np.mean(methods.onetoonedist(refResult.centroids, sigFeature.centroids),axis=0)

    sigNames.append(sigFeature.sigNo)
    # distBlacks.append(np.sum(methods.onetoonedist(refResult.blacks, sigFeature.blacks)))
    # distAngles.append(np.sum(methods.onetoonedist(refResult.angles, sigFeature.angles)))
    # distNormalizedSize.append(np.sum(methods.onetoonedist(refResult.normalizedSize, sigFeature.normalizedSize)))
    # distNormalizedSumOfAngles.append(np.sum(methods.onetoonedist(refResult.normalizedSumOfAngles,sigFeature.normalizedSumOfAngles)))
    # distRatios.append(np.sum(methods.onetoonedist(refResult.ratios, sigFeature.ratios)))
    # distTransitions.append(np.sum(methods.onetoonedist(refResult.transitions, sigFeature.transitions)))
    # distCentroids.append(np.sum(methods.onetoonedist(refResult.centroids, sigFeature.centroids)))
    txt = sigFeature.sigNo
    if txt == 49 or txt == 52 or txt == 66:
        colors.append('red')
    else:
        colors.append('black')
    distAngles.append(np.mean(sigFeature.angles))
    distNormalizedSize.append(np.mean(sigFeature.normalizedSize))
    distNormalizedSumOfAngles.append(np.mean(sigFeature.normalizedSumOfAngles))
    distRatios.append(np.mean(sigFeature.ratios))
    distTransitions.append(np.mean(sigFeature.transitions))
    distCentroids.append(np.mean(sigFeature.centroids))



    

    # distList['D{:02d}{:02d}'.format(refSigNo, sigFeature.sigNo)] = {
    #     'distBacks': distBlacks,
    #     'distAngles': distAngles,
    #     'distNormalizedSize': distNormalizedSize,
    #     'distNormalizedSumOfAngles': distNormalizedSumOfAngles,
    #     'distRatios': distRatios,
    #     'distTransitions': distTransitions,
    #     'distCentroids': distCentroids

    # }
    # distAggregate['D{:02d}{:02d}'.format(refSigNo, sigFeature.sigNo)] = distAngles +\
    #     distRatios + \
    #     distTransitions +\
    #     distNormalizedSize +\
    #     distNormalizedSumOfAngles +\
    #     distCentroids



# colors.append('red')
# sigNames.append('original')
# distAngles.append(np.mean(refResult.angles))
# distNormalizedSize.append(np.mean(refResult.normalizedSize))
# distNormalizedSumOfAngles.append(np.mean(refResult.normalizedSumOfAngles))
# distRatios.append(np.mean(refResult.ratios))
# distTransitions.append(np.mean(refResult.transitions))
# distCentroids.append(np.mean(refResult.centroids))




featureVectors = {
    'f1':distAngles,
    'f2':distNormalizedSize,
    'f3':distNormalizedSumOfAngles,
    'f4':distRatios,
    'f5':distCentroids,
    'f6':distBlacks,
    'f7':distTransitions
}


def showPlot(f1,f2,colors):
        
    # pp(distList)

    # lists = sorted(distAggregate.items())  # sorted by key, return a list of tuples

    # # x, y = zip(*lists)  # unpack a list of pairs into two tuples

    # plt.plot(x, y)
    # plt.show()

    # colors = (0,0,0)
    area = np.pi*3
    plt.title('Scatter plot offline signature verification')
    plt.xlabel('x')
    plt.ylabel('y')


    x = f1
    y = f2

    # , s=area, c=colors, alpha=0.5
    plt.scatter(x, y,None,colors)

    # for i, txt in enumerate(sigNames):
    #     if txt == 49 or txt == 52 or txt == 66:
    #         txt = 'genuine'
    #     plt.annotate(txt, (x[i],y[i]))
        

    plt.show()
    # plt.figure().clf()


    # genuine sig 49 52 66



for f1,f2 in itertools.product(featureVectors.keys(),featureVectors.keys()):
    showPlot(featureVectors.get(f1),featureVectors.get(f2),colors)