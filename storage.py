

import os
import numpy as np


def store(path,groupNo, sigNo, centroids=None, transitions=None, ratios=None, angles=None, blacks=None, normalizedSize=None, normalizedSumOfAngles=None):


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
               sigNoToFileName(groupNo,sigNo), centroids, fmt='%d')
    np.savetxt(path + '/transitions/'+sigNoToFileName(groupNo,sigNo), transitions)
    np.savetxt(path + '/ratios/'+sigNoToFileName(groupNo,sigNo), ratios)
    np.savetxt(path + '/angles/'+sigNoToFileName(groupNo,sigNo), angles)
    np.savetxt(path + '/blacks/'+sigNoToFileName(groupNo,sigNo), blacks, fmt='%d')
    np.savetxt(path + '/normalizedSize/' +
               sigNoToFileName(groupNo,sigNo), normalizedSize)
    np.savetxt(path + '/normalizedSumOfAngles/' +
               sigNoToFileName(groupNo,sigNo), normalizedSumOfAngles)




def get(path,groupNo, sigNo, feature):
    return np.genfromtxt(path + '/' + feature + '/' + sigNoToFileName(groupNo,sigNo))


def get(path,groupNo, sigNo, feature):
    return np.genfromtxt(path + '/' + feature + '/' + sigNoToFileName(groupNo,sigNo))


def sigNoToFileName(group,sigNo):
    return '{group}_{sigNo}'.format(group=group, sigNo=sigNo)
