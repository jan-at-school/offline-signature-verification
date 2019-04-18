from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
from feature_extractor import FeatureExtractor
import numpy as np
import methods
import os

'''
data set
http://www.cedar.buffalo.edu/NIJ/data/signatures.rar
'''


allsigfiles = os.listdir('res')

print(allsigfiles)

for i in range(len(allsigfiles)):
    sig = "R{:03d}".format(i)
    print(sig)

    filename, file_extension = os.path.splitext(allsigfiles[i])
    if file_extension == '.png' or file_extension == '.jpg':
        FeatureExtractor('res/'+ allsigfiles[i],sig, i).extract()
