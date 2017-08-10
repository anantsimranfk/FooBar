import operator
import requests
import numpy as np
import ast
from numpy.linalg import norm

# conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="", db="foobar")
# c = conn.cursor()
imageVsScore = {}

def getSimilarImages(trendId, imageUrls):
    centroid = getCentroid(imageUrls)
    candidateImages = getCandidateImages(trendId)
    calculateScores(centroid,candidateImages)
    bestImages = getBestImages(5)
    return bestImages

def getCentroid(trendImages):
    numberOfImages = len(trendImages)
    centroid = np.zeros(4096)
    for i in range(numberOfImages):
        imageFeature = ast.literal_eval(getFeatureStringForImage(trendImages[i]))
        centroid = centroid + imageFeature
    return centroid

def getFeatureStringForImage(url):
    apiUrl = "http://10.33.49.81:9001/v2/extract_by_url/image-matching-001"
    response = requests.post(apiUrl,json={"url":url})
    featureString = response.content
    return featureString

def similarityScore(centroid,imageFeature):
    cos_sim = np.dot(centroid, imageFeature)/(norm(centroid)*norm(imageFeature))
    return cos_sim

def calculateScores(centroid,candidateImages):
    numberOfImages = len(candidateImages)
    for i in range(numberOfImages):
        imageFeature = ast.literal_eval(getFeatureStringForImage(candidateImages[i]))
        imageVsScore[candidateImages[i]]=similarityScore(centroid,imageFeature)

def getBestImages(k):
    bestImages = []
    sorted_scores = sorted(imageVsScore.items(), key=operator.itemgetter(1))
    for i in range(k):
        bestImages.append(sorted_scores[i][0])

def updateModel(trendId, checkedImageUrls):
    pass

def initializeModel(trendId,trendImages):
    pass