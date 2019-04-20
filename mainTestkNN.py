
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


# class KNNTest:


resFilePath = 'res'
inputFiles = os.listdir(resFilePath)
totalSigs = len(os.listdir('processed/centroids'))

questionedSig = 'data/test/forgeries_{person}_{signNo}'.format(person=1, signNo=5)


refResult = feature_extractor.FeatureExtractor(questionedSig,None,None,None).extract()






for i in range(totalSigs):
    if(i ==)
