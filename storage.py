

import os
import numpy as np
import feature_extractor
import re

PROCESSED_PATH = 'processed'

def store(path,groupNo, sigNo,sigFeatures):
    

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
               sigNoToFileName(groupNo,sigNo), sigFeatures.centroids, fmt='%d')
    np.savetxt(path + '/transitions/'+sigNoToFileName(groupNo,sigNo), sigFeatures.transitions)
    np.savetxt(path + '/ratios/'+sigNoToFileName(groupNo,sigNo), sigFeatures.ratios)
    np.savetxt(path + '/angles/'+sigNoToFileName(groupNo,sigNo), sigFeatures.angles)
    np.savetxt(path + '/blacks/'+sigNoToFileName(groupNo,sigNo), sigFeatures.blacks, fmt='%d')
    np.savetxt(path + '/normalizedSize/' +
               sigNoToFileName(groupNo,sigNo), sigFeatures.normalizedSize)
    np.savetxt(path + '/normalizedSumOfAngles/' +
               sigNoToFileName(groupNo,sigNo), sigFeatures.normalizedSumOfAngles)



def getDataSetCount():
    return len(os.listdir('processed' + '/' + 'angles'))


def getProcessedSig(groupNo, sigNo):
    path = PROCESSED_PATH
    sigFeatures = feature_extractor.SigFeatures(groupNo,sigNo)
    sigFeatures.angles = np.genfromtxt(path + '/' + 'angles' + '/' + sigNoToFileName(groupNo,sigNo))
    sigFeatures.centroids = np.genfromtxt(path + '/' + 'centroids' + '/' + sigNoToFileName(groupNo,sigNo))
    sigFeatures.blacks = np.genfromtxt(path + '/' + 'blacks' + '/' + sigNoToFileName(groupNo,sigNo))
    sigFeatures.normalizedSize = np.genfromtxt(path + '/' + 'normalizedSize' + '/' + sigNoToFileName(groupNo,sigNo))
    sigFeatures.normalizedSumOfAngles = np.genfromtxt(path + '/' + 'normalizedSumOfAngles' + '/' + sigNoToFileName(groupNo,sigNo))
    sigFeatures.ratios = np.genfromtxt(path + '/' + 'ratios' + '/' + sigNoToFileName(groupNo,sigNo))

    return sigFeatures

def getProcessedSigFeature(groupNo, sigNo, feature):
    return np.genfromtxt(PROCESSED_PATH + '/' + feature + '/' + sigNoToFileName(groupNo,sigNo))

def getAllProcessed():
    alll = list()
    allAnglesProcessed = os.listdir('processed' + '/' + 'angles')
    for filename in allAnglesProcessed:
        groupNo,sigNo = re.findall('\d+',filename) 
        alll.append(getProcessedSig(groupNo,sigNo))

    return alll

def sigNoToFileName(group,sigNo):
    return '{group}_{sigNo}.txt'.format(group=group, sigNo=sigNo)
