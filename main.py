from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
from feature_extractor import FeatureExtractor
import numpy as np
import methods
import os





allsigfiles = os.listdir('res')



for i in range(len(allsigfiles)):
    if i != 0:
        sig = "R{:03d}".format(i)
        FeatureExtractor('res',sig,'.png').extract()
    

