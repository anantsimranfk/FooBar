import NetworkHandler
import requests

fsns = NetworkHandler.getProductIds("t_shirt")

testFSNs = []
for fsn in fsns:
    response = requests.get("http://10.85.51.84/sp-cms-backend/rest/entity/product/" + fsn)
    try:
        if response.json()[fsn]["productCommonData"]["productAttributes"]["pattern"]["valuesList"][0]["value"] == "Floral Print":
            testFSNs.append(fsn)
    except KeyError:
        pass

print testFSNs

print NetworkHandler.getImages(testFSNs)
