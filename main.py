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


NO_OF_THREADS = 50

inputFilesPath = storage.DATASET_PATH + '/TestSet/Questioned'
# inputFilesPath = 'res'
allsigfiles = os.listdir(inputFilesPath)
totalSigs = len(allsigfiles)
print(allsigfiles)
print(totalSigs)

threads = list()

startTime = time.time()

for i, file in enumerate(allsigfiles):
    filename, file_extension = os.path.splitext(file)

    if file_extension == '.png' or file_extension == '.jpg':
        print(filename)

        sigNo = re.findall('\d+', filename)
        sigNo = int(sigNo[0])
        #  filePath, groupNo, sigNo, progress, totalSigs

        if NO_OF_THREADS > 1:
            threads.append(feature_extractor.FeatureExtractorThread(
                inputFilesPath+'/'+file, sigNo, totalSigs))
        else:
            feature_extractor.FeatureExtractor(
                inputFilesPath+'/'+file, sigNo).extractAndSave()


if NO_OF_THREADS > 1:
    print('Starting Threads')
    for thread in threads:
        while threading.active_count() > NO_OF_THREADS:
            time.sleep(1)
        thread.start()

    # wait for all of them to complete
    for thread in threads:
        thread.join()


alll = storage.getAllProcessed()

# print(alll)


print(time.time() - startTime)
