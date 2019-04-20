
from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import numpy as np
import methods
from math import atan
import os
import math
from feature_extractor import FeatureExtractor
import storage


# class KNNTest:


resFilePath = 'res'
inputFiles = os.listdir(resFilePath)
totalSigs = len(os.listdir('processed/centroids'))

refResult = FeatureExtractor(, None).extract()



for i in range(totalSigs):
    if(i == )