import requests
from sets import Set


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


MAX_FETCH_IDS = 5000
PADDING_IDS = 2000;

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
            except ValueError:
                pass
    return images


def getProductIds(vertical):
    max_product_version = requests.get("http://10.85.51.84/sp-cms-backend/rest/entity/verticalVersion").json()[vertical]
    fromVersion = max(0, max_product_version - MAX_FETCH_IDS - PADDING_IDS)
    requestString = "http://10.85.132.32:26600/sp-cms-backend/rest/entity/delta/v2/" + vertical + "?fromVersion="
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


print getImages(getProductIds("t_shirt"))