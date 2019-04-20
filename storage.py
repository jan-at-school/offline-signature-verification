

import os
import numpy as np


def store(path, sigNo, centroids=None, transitions=None, ratios=None, angles=None, blacks=None, normalizedSize=None, normalizedSumOfAngles=None):


    if not os.path.exists(path + '/centroids'):
        os.makedirs(path + '/centroids')
    if not os.path.exists(path + '/transitions'):
        os.makedirs(path + '/transitions')
    if not os.path.exists(path + '/ratios'):
        os.makedirs(path + '/ratios')
    if not os.path.exists(path + '/angles'):
        os.makedirs(path + '/angles')
    if not os.path.exists(path + '/blacks'):
        os.makedirs(path + '/blacks')
    if not os.path.exists(path + '/normalizedSize'):
        os.makedirs(path + '/normalizedSize')
    if not os.path.exists(path + '/normalizedSumOfAngles'):
        os.makedirs(path + '/normalizedSumOfAngles')

    np.savetxt(path + '/centroids/' +
               sigNoToFileName(sigNo), centroids, fmt='%d')
    np.savetxt(path + '/transitions/'+sigNoToFileName(sigNo), transitions)
    np.savetxt(path + '/ratios/'+sigNoToFileName(sigNo), ratios)
    np.savetxt(path + '/angles/'+sigNoToFileName(sigNo), angles)
    np.savetxt(path + '/blacks/'+sigNoToFileName(sigNo), blacks, fmt='%d')
    np.savetxt(path + '/normalizedSize/' +
               sigNoToFileName(sigNo), normalizedSize)
    np.savetxt(path + '/normalizedSumOfAngles/' +
               sigNoToFileName(sigNo), normalizedSumOfAngles)


def get(path, sigNo, feature):
    return np.genfromtxt(path + '/' + feature + '/' + sigNoToFileName(sigNo))


def sigNoToFileName(sigNo):
    return "R{:03d}".format(sigNo)
