import ClassifierUtils
import NetworkHandler
import time
import SVMClassifier
import json

fp = open("fp.json", "w")
fn = open("fn.json", "w")


def getProductScores(number, vertical, positiveImages, negativeImages):
    start = time.time()
    featureVectorsPositive = NetworkHandler.getFeatureVectors(positiveImages)
    print str(time.time() - start) + " :Got feature vectors for positive"
    fp.write(json.dumps(featureVectorsPositive))
    fp.close()
    featureVectorsNegative = NetworkHandler.getFeatureVectors(negativeImages)
    print str(time.time() - start) + " :Got feature vectors for negative"
    fn.write(json.dumps(featureVectorsNegative))
    fn.close()
    # featureVectorsNegative = json.loads(fn.read())
    # featureVectorsPositive = json.loads(fp.read())

    clf = SVMClassifier.classify(featureVectorsNegative, featureVectorsPositive)
    print str(time.time() - start) + " :Classified model"

    x = SVMClassifier.getClassified(clf, NetworkHandler.getFeatureVector(
        "http://img.fkcdn.com/image/j1dvte80/t-shirt/n/h/x/m-1704589-roadster-original-imaestkmxzsefj8w.jpeg"))

    fsns = NetworkHandler.getProductIds(vertical)
    images = NetworkHandler.getImages(fsns)
    print str(time.time() - start) + " :Got images"
    featureVectors = NetworkHandler.getFeatureVectors(images)
    print str(time.time() - start) + " :Got featureVectors"
    productScores = {}
    for i in range(len(images)):
        productScores[fsns[i]] = SVMClassifier.getClassified(clf, featureVectors[i])[0]
        print str(time.time() - start) + " :Processed Image" + str(i)
    return ClassifierUtils.getBestItems(number, productScores)


# print getProductScores(15, "sandal", [
#     "http://img.fkcdn.com/image/832/832/j4rc8sw0/sandal/9/e/5/130p909-35-klaur-melbourne-red-original-imaevhqkafzrg7yt.jpeg?q=70",
#     "http://img.fkcdn.com/image/832/832/sandal/n/v/2/beige-f-2617-kielz-41-original-imaezpzm8es6thth.jpeg?q=70",
#     "http://img.fkcdn.com/image/832/832/sandal/q/s/b/pink-fnh-5825-j6-flat-n-heels-39-original-imaepz9yhdysars2.jpeg?q=70"])

# getProductScores(20,"t_shirt",0,0)


def getProductScoresV2(number, vertical, positiveFSNs):
    start = time.time()
    frequencyDict = NetworkHandler.getFrequencyDict(positiveFSNs)
    print str(time.time() - start) + " :Got data for precomputed FSNs"
    prec = open("precompute.json", "w")
    # prec.write(json.dumps(frequencyDict))
    fsns = NetworkHandler.getProductIds(vertical)
    scores = NetworkHandler.getIndividualScores(frequencyDict, fsns)
    print str(time.time() - start) + " :Got score "
    productScores = {}
    for i in range(len(scores)):
        productScores[fsns[i]] = scores[i]
    return ClassifierUtils.getBestItems(number, productScores)

