import ClassifierUtils
import NetworkHandler


def getProductScores(number, vertical, trainedImages):
    centroid = ClassifierUtils.getCentroid(map(NetworkHandler.getFeatureVector, trainedImages))
    print "got centroid"
    fsns = NetworkHandler.getProductIds(vertical)
    images = NetworkHandler.getImages(fsns)
    print "Got images"
    productScores = {}
    for i in range(len(images)):
        productScores[fsns[i]] = ClassifierUtils.getSimilarityScore(centroid,
                                                                    NetworkHandler.getFeatureVector(images[i]))
        print "Processed Image" + str(i)
    return ClassifierUtils.getBestItems(number, productScores)


# print getProductScores(15, "sandal", [
#     "http://img.fkcdn.com/image/832/832/j4rc8sw0/sandal/9/e/5/130p909-35-klaur-melbourne-red-original-imaevhqkafzrg7yt.jpeg?q=70",
#     "http://img.fkcdn.com/image/832/832/sandal/n/v/2/beige-f-2617-kielz-41-original-imaezpzm8es6thth.jpeg?q=70",
#     "http://img.fkcdn.com/image/832/832/sandal/q/s/b/pink-fnh-5825-j6-flat-n-heels-39-original-imaepz9yhdysars2.jpeg?q=70"])
