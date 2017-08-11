from sklearn import svm
import NetworkHandler


def classify(negativeData, positiveData):
    negativeData = [n for n in negativeData if n != -1]
    positiveData = [n for n in positiveData if n != -1]
    y = []
    for i in range(len(negativeData)):
        y.append(0)
    for i in range(len(positiveData)):
        y.append(1)
    negativeData.extend(positiveData)
    clf = svm.SVC(gamma=0.0000007, kernel='rbf', verbose=True,C=2.0)
    clf.fit(negativeData, y)
    print "Trained data"
    return clf


def getClassified(clf, featureVector):
    if featureVector == -1:
        return 0
    predict = clf.predict(featureVector)
    return predict
