from PIL import Image
import itertools
from PIL import ImageDraw
from methods import BOX
import feature_extractor
# from feature_extrator_thread import
import numpy as np
import methods
import os
import storage
import time
import re
import threading
'''
data set
http://www.cedar.buffalo.edu/NIJ/data/signatures.rar
'''


inputFilesPath = 'res'
allsigfiles = os.listdir(inputFilesPath)
totalSigs = len(allsigfiles)
print(allsigfiles)
print(totalSigs)

threads = list()


for i, file in enumerate(allsigfiles):
    filename, file_extension = os.path.splitext(file)

    if file_extension == '.png' or file_extension == '.jpg':
        print(filename)
        
        groupNo,sigNo = re.findall('\d+',filename) 
        #  filePath, groupNo, sigNo, progress, totalSigs
        threads.append(feature_extractor.FeatureExtractorThread(inputFilesPath+'/'+file,groupNo,sigNo, i, totalSigs))

print('Starting Threads')

for thread in threads:
    while threading.active_count() > 150:
        time.sleep(5)
    thread.start()

# wait for all of them to complete
for thread in threads:
    thread.join()


centroids = storage.get(1, 10, 'ratios')

print(centroids)
