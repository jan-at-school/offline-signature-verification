

import os
import numpy as np
import feature_extractor
import re


DATASET_PATH = 'dataset'
PROCESSED_PATH = 'processed'


def store(path, sigNo, sigFeatures):

    path = 'processed'
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
               sigNoToFileName(sigNo), sigFeatures.centroids, fmt='%d')
    np.savetxt(path + '/transitions/'+sigNoToFileName(sigNo),
               sigFeatures.transitions)
    np.savetxt(path + '/ratios/'+sigNoToFileName(sigNo), sigFeatures.ratios)
    np.savetxt(path + '/angles/'+sigNoToFileName(sigNo), sigFeatures.angles)
    np.savetxt(path + '/blacks/'+sigNoToFileName(sigNo),
               sigFeatures.blacks, fmt='%d')
    np.savetxt(path + '/normalizedSize/' +
               sigNoToFileName(sigNo), sigFeatures.normalizedSize)
    np.savetxt(path + '/normalizedSumOfAngles/' +
               sigNoToFileName(sigNo), sigFeatures.normalizedSumOfAngles)


def getDataSetCount():
    return len(os.listdir('processed' + '/' + 'angles'))


def getProcessedSig(sigNo):
    path = PROCESSED_PATH
    sigFeatures = feature_extractor.SigFeatures(sigNo)
    sigFeatures.angles = np.genfromtxt(
        path + '/' + 'angles' + '/' + sigNoToFileName(sigNo))
    sigFeatures.centroids = np.genfromtxt(
        path + '/' + 'centroids' + '/' + sigNoToFileName(sigNo))
    sigFeatures.blacks = np.genfromtxt(
        path + '/' + 'blacks' + '/' + sigNoToFileName(sigNo))
    sigFeatures.normalizedSize = np.genfromtxt(
        path + '/' + 'normalizedSize' + '/' + sigNoToFileName(sigNo))
    sigFeatures.normalizedSumOfAngles = np.genfromtxt(
        path + '/' + 'normalizedSumOfAngles' + '/' + sigNoToFileName(sigNo))
    sigFeatures.ratios = np.genfromtxt(
        path + '/' + 'ratios' + '/' + sigNoToFileName(sigNo))

    return sigFeatures


def getProcessedSigFeature(sigNo, feature):
    return np.genfromtxt(PROCESSED_PATH + '/' + feature + '/' + sigNoToFileName(sigNo))


def getAllProcessed():
    alll = list()
    allAnglesProcessed = os.listdir(PROCESSED_PATH + '/' + 'angles')
    for filename in allAnglesProcessed:
        sigNo = re.findall('\d+', filename)
        alll.append(getProcessedSig(int(sigNo[0])))

    return alll


def sigNoToFileName(sigNo):
    return 'P{:03d}.txt'.format(sigNo)
