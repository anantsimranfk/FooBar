import operator
import requests
import numpy as np
from numpy.linalg import norm

# conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="", db="foobar")
# c = conn.cursor()

imageVsScore = {}


def getCentroid(featureVectors):
    featureVectors = [featureVector for featureVector in featureVectors if featureVector != -1]
    return np.mean(np.array(featureVectors), axis=0)


def getSimilarityScore(centroid, imageFeature):
    if imageFeature == -1:
        return 10000;
    centroid = np.array(centroid)
    imageFeature = np.array(imageFeature)
    cos_sim = 1 - np.dot(centroid, imageFeature) / (norm(centroid) * norm(imageFeature))
    return cos_sim


def getBestItems(k, myDict):
    bestItems = []
    sorted_scores = sorted(myDict.items(), key=operator.itemgetter(1))
    for i in range(k):
        if i == len(sorted_scores):
            break
        bestItems.append(sorted_scores[i])
    return bestItems

# def getSimilarImages(trendId, imageUrls):
#     centroid = getCentroid(imageUrls)
#     candidateImages = getCandidateImages(trendId)
#     calculateScores(centroid, candidateImages)
#     bestImages = getBestImages(5)
#     return bestImages
#
#
# def calculateScores(centroid, candidateImages):
#     numberOfImages = len(candidateImages)
#     for i in range(numberOfImages):
#         imageFeature = ast.literal_eval(getFeatureStringForImage(candidateImages[i]))
#         imageVsScore[candidateImages[i]] = getSimilarityScore(centroid, imageFeature)



# def updateModel(trendId, checkedImageUrls):
#     pass
#
#
# def initializeModel(trendId, trendImages):
#     pass
