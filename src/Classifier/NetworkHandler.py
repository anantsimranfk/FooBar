import requests
from sets import Set
from multiprocessing.dummy import Pool as ThreadPool
import ClassifierUtils
from functools import partial


POOL_SIZE = 60
MAX_FETCH_IDS = 5000
PADDING_IDS = 2000


def getFrequencyDict(fsns):
    frequencyDict = {"pattern": {}, "type": {}, "trend": {}, "theme": {}, "color": {}}
    imageList=[]
    for fsn in fsns:
        response = requests.get("http://10.85.51.84/sp-cms-backend/rest/entity/product/" + fsn)
        try:
            pattern = response.json()[fsn]["productCommonData"]["productAttributes"]["pattern"]["valuesList"][0][
                "value"]
            if frequencyDict["pattern"].get(pattern) is None:
                frequencyDict["pattern"][pattern] = 0
            frequencyDict["pattern"][pattern] = frequencyDict["pattern"][pattern] + 1
        except KeyError:
            pass
        try:
            type = response.json()[fsn]["productCommonData"]["productAttributes"]["type"]["valuesList"][0]["value"]
            if frequencyDict["type"].get(type) is None:
                frequencyDict["type"][type] = 0
            frequencyDict["type"][type] = frequencyDict["type"][type] + 1
        except KeyError:
            pass
        try:
            trend = response.json()[fsn]["productCommonData"]["productAttributes"]["trend"]["valuesList"][0]["value"]
            if frequencyDict["trend"].get(trend) is None:
                frequencyDict["trend"][trend] = 0
            frequencyDict["trend"][trend] = frequencyDict["trend"][trend] + 1
        except KeyError:
            pass
        try:
            theme = response.json()[fsn]["productCommonData"]["productAttributes"]["theme"]["valuesList"][0]["value"]
            if frequencyDict["theme"].get(theme) is None:
                frequencyDict["theme"][theme] = 0
            frequencyDict["theme"][theme] = frequencyDict["theme"][theme] + 1
        except KeyError:
            pass
        try:
            color = response.json()[fsn]["productCommonData"]["productAttributes"]["color"]["valuesList"][0]["value"]
            if frequencyDict["color"].get(color) is None:
                frequencyDict["color"][color] = 0
            frequencyDict["color"][color] = frequencyDict["color"][color] + 1
        except KeyError:
            pass
        try:
            imageList.append(
                response.json()[fsn]["productCommonData"]["staticContentInfo"][0]["transContents"][0]["s3_path"][
                    "valuesList"][0]["value"])
        except KeyError:
            pass
    frequencyDict["centroid"]= ClassifierUtils.getCentroid(getFeatureVectors(imageList))
    return frequencyDict


def getIndividualScore(fsn,frequencyDict):
    score=0
    response = requests.get("http://10.85.51.84/sp-cms-backend/rest/entity/product/" + fsn)
    try:
        score += frequencyDict["pattern"][
            response.json()[fsn]["productCommonData"]["productAttributes"]["pattern"]["valuesList"][0]["value"]]
    except KeyError:
        pass
    try:
        score += frequencyDict["type"][
            response.json()[fsn]["productCommonData"]["productAttributes"]["type"]["valuesList"][0]["value"]]
    except KeyError:
        pass
    try:
        score += frequencyDict["trend"][
            response.json()[fsn]["productCommonData"]["productAttributes"]["trend"]["valuesList"][0]["value"]]
    except KeyError:
        pass
    try:
        score += frequencyDict["theme"][
            response.json()[fsn]["productCommonData"]["productAttributes"]["theme"]["valuesList"][0]["value"]]
    except KeyError:
        pass
    try:
        score += frequencyDict["color"][
            response.json()[fsn]["productCommonData"]["productAttributes"]["color"]["valuesList"][0]["value"]]
    except KeyError:
        pass
    try:
        score += 1000 * ClassifierUtils.getSimilarityScore(frequencyDict["centroid"], getFeatureVector(
            response.json()[fsn]["productCommonData"]["staticContentInfo"][0]["transContents"][0]["s3_path"]["valuesList"][
                0]["value"]))
    except KeyError:
        pass
    return score


def getIndividualScores(frequencyDiction,fsns):
    pool = ThreadPool(POOL_SIZE)
    mapfunc = partial(getIndividualScore, frequencyDict=frequencyDiction)
    scores = pool.map(mapfunc, fsns)
    pool.close()
    pool.join()
    return scores



def getFeatureVector(url):
    apiUrl = "http://10.33.49.81:9001/v2/extract_by_url/image-matching-001"
    response = requests.post(apiUrl, json={"url": url})
    try:
        featureString = response.json()["result"]["fv"]
    except KeyError:
        print "Could not process URL :" + url
        return -1
    return featureString


def getFeatureVectors(urls):
    pool = ThreadPool(POOL_SIZE)
    vectors = pool.map(getFeatureVector, urls)
    pool.close()
    pool.join()
    return vectors


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


zuluHeaders = {'z-clientId': 'zulu.admin',
               'z-requestId': 'abc',
               'z-timestamp': '123'}


def getImages(productIDs):
    groupedIds = list(chunks(productIDs, 39))
    images = []
    for group in groupedIds:
        response = requests.get("http://10.47.1.8:31200/views?viewNames=product_base_info&entityIds=" + ",".join(group),
                                headers=zuluHeaders)
        for view in response.json()["entityViews"]:
            try:
                images_given = view["view"]["static_images"]
                primary_image_id = view["view"]["primary_image_id"]
                for image in images_given:
                    if primary_image_id.lower() in image.lower():
                        images.append(image)
                        break
            except ValueError:
                pass
    return images


def getProductIds(vertical):
    max_product_version = requests.get("http://10.85.51.84/sp-cms-backend/rest/entity/verticalVersion").json()[vertical]
    fromVersion = max(0, max_product_version - MAX_FETCH_IDS - PADDING_IDS)
    requestString = "http://10.85.132.32:26600/sp-cms-backend/rest/entity/delta/v2/" + vertical + "?limit=" + str(
        MAX_FETCH_IDS) + "&fromVersion="
    fsns = Set()
    while len(fsns) < MAX_FETCH_IDS:
        response = requests.get(requestString + str(fromVersion))
        if not response.status_code == 200:
            break
        for productVersion in response.json()["productVersionList"]:
            fsns.add(productVersion["first"])
        if not response.json()["hasMore"]:
            break
        fromVersion = response.json()["nextVersionNumber"]
    return list(set(fsns))
