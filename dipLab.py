'''
Requirments:
  python &
  > pip install pillow
  > pip install matplotlib
  > pip install numpy
Run:
  > python task1.py path/to/image
'''

import PIL
from PIL import Image
import numpy as np
import itertools
import sys
import os
import matplotlib.pyplot as plt
import mylib
from mylib import BOX


# open image
# you have to pass the input image path as input arg
image = Image.open(sys.argv[1])
image = image.convert("L")  # convert to signle channeled image

image2 = Image.open(sys.argv[1])
image2 = image.convert("L")  # only for reading purposes
width, height = image.size
totalPixels = width * height

minWindowSize = int(sys.argv[3])
windowSize = minWindowSize

while not height % windowSize == 0 and not width % windowSize == 0:
    windowSize += 1

stride = int(sys.argv[4])

outDir = sys.argv[2] + '/windowsize_'+ str(windowSize) +'_stride_'+ str(stride)

if not os.path.exists(outDir):
    os.makedirs(outDir)



freq = [0] * 256  # fill
cProbability = [0] * 256  # fill zeros


# save original image histogram
freq = image.histogram()
a = np.array(image)
plt.hist(a.ravel(),  bins=256)
plt.ylabel('Probability')
plt.xlabel('Gray Level')

image.save(outDir+'/input.jpg')
plt.savefig(outDir+'/inputhist.svg')
plt.show()


centerX, centerY = (int(width/2), int(height/2))


print('Found the window size to be '+ str(windowSize))
# # keep x, y the start of the window and let the size of the window determine the box size
# for x, y in itertools.product(range(width), range(height)):
#     image = mylib.equalizeHistogram(image, editableImage, BOX(x, y, x + windowSize if (x + windowSize) <= width else width, y + windowSize if (y + windowSize) <= height else height))


threads = list()
editableImage = image.load()
# keep x, y the start of the window and let the size of the window determine the box size
for x, y in itertools.product(range(int(width/stride)), range(int(height/stride))):
  x = x * stride
  y = y * stride
  threads.append(mylib.EqualizeWindowThread(image2, editableImage,
                                              BOX(x, y, x + windowSize if (x + windowSize) <= width else width, y + windowSize if (y + windowSize) <= height else height)))


# initialize array before starting threads
for thread in threads:
    thread.start()

# wait for all of them to complete
for thread in threads:
    thread.join()

image.save(outDir+'/output.jpg')
a = np.array(image)
plt.hist(a.ravel(),  bins=256)
plt.savefig(outDir+'/outputhist.svg')
plt.show()