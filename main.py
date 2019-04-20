from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
from feature_extractor import FeatureExtractor
import numpy as np
import methods
import os
import storage
'''
data set
http://www.cedar.buffalo.edu/NIJ/data/signatures.rar
'''


inputFilesPath = 'res'
allsigfiles = os.listdir(inputFilesPath)

totalSigs = len(allsigfiles)
print(allsigfiles)
print(totalSigs)
for i, file in enumerate(allsigfiles):
    print(i, 'out if', totalSigs)
    filename, file_extension = os.path.splitext(file)

    if file_extension == '.png' or file_extension == '.jpg':
        print(file)
        FeatureExtractor(inputFilesPath+'/'+file, sigNo=i).extractAndSave()


centroids = storage.get('processed', 1, 'ratios')

print(centroids)
