import ClassifierUtils
import NetworkHandler
import time

def getProductScores(number, vertical, trainedImages):
    featureVectors = NetworkHandler.getFeatureVectors(trainedImages)
    centroid = ClassifierUtils.getCentroid(featureVectors)
    print "got centroid"
    fsns = NetworkHandler.getProductIds(vertical)
    images = NetworkHandler.getImages(fsns)
    print "Got images"
    featureVectors = NetworkHandler.getFeatureVectors(images)
    productScores = {}
    for i in range(len(images)):
        productScores[fsns[i]] = ClassifierUtils.getSimilarityScore(centroid,featureVectors[i])
        print "Processed Image" + str(i)
    return ClassifierUtils.getBestItems(number, productScores)

start = time.time()
print("hello")

print getProductScores(15, "sandal", [
    "http://img.fkcdn.com/image/832/832/j4rc8sw0/sandal/9/e/5/130p909-35-klaur-melbourne-red-original-imaevhqkafzrg7yt.jpeg?q=70",
    "http://img.fkcdn.com/image/832/832/sandal/n/v/2/beige-f-2617-kielz-41-original-imaezpzm8es6thth.jpeg?q=70",
    "http://img.fkcdn.com/image/832/832/sandal/q/s/b/pink-fnh-5825-j6-flat-n-heels-39-original-imaepz9yhdysars2.jpeg?q=70"])

end = time.time()
print(end - start)
