
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


print(storage.getDataSetCount())
processedData = storage.getAllProcessed()


blacks = list()
angles = list()
normalizedSize = list()
normalizedSumOfAngles = list()
ratios = list()
transitions = list()
centroids = list()


distAggregate = dict()
sigNames = list()
colors = list()
for sigFeature in processedData:

    sigNames.append(sigFeature.sigNo)

    txt = sigFeature.sigNo
    if txt == 49 or txt == 52 or txt == 66:
        colors.append('red')
    else:
        colors.append('black')
    angles.append(np.mean(sigFeature.angles))
    blacks.append(np.mean(sigFeature.blacks))
    normalizedSize.append(np.mean(sigFeature.normalizedSize))
    normalizedSumOfAngles.append(np.mean(sigFeature.normalizedSumOfAngles))
    ratios.append(np.mean(sigFeature.ratios))
    transitions.append(np.mean(sigFeature.transitions))
    centroids.append(np.mean(sigFeature.centroids))


featureVectors = {
    'f1': {
        'name': 'angles',
        'value': angles
    },
    'f2': {
        'name': 'normalizedSize',
        'value': normalizedSize
    },
    'f3': {
        'name': 'normalizedSumOfAngles',
        'value': normalizedSumOfAngles
    },
    'f4': {
        'name': 'ratios',
        'value': ratios
    },
    'f5': {
        'name': 'centroids',
        'value': centroids
    },
    'f6': {
        'name': 'blacks',
        'value': blacks
    },
    'f7': {
        'name': 'transitions',
        'value': transitions
    }
}



def savePlot(f1, f2, colors):

    plt.title('Scatter plot offline signature verification')
    plt.xlabel(f1.get('name'))
    plt.ylabel(f2.get('name'))

    x = f1.get('value')
    y = f2.get('value') # value contains the data

    print('sizes',len(x),len(y))
    plt.scatter(x, y, None, colors)
    

    plt.savefig('featurePlots/{f1}_{f2}.png'.format(f1=f1.get('name'),f2=f2.get('name')))
    


    # genuine sig 49 52 66


for f1, f2 in itertools.product(featureVectors.keys(), featureVectors.keys()):
    print(f1, f2)
    
    if not os.path.exists('featurePlots'):
        os.makedirs('featurePlots')
    print(featureVectors.get(f1).get('name'), featureVectors.get(f2).get('name'))
    savePlot(featureVectors.get(f1), featureVectors.get(f2), colors)




