import web
import json
import ClassifierService
import NetworkHandler
import requests
from threading import Thread

urls = (
    '/similarImages', 'index',
    '/v3', 'v3',
    '/v2', 'v2',
    '/hello', 'hello'
)

SETU_MACHINE_IP ="http://172.20.44.122:8080/"


def JobScheduler(trendId, vertical, fsns):
    print "Job started with " + str(trendId) + " " + str(vertical) + " " + str(fsns)
    products = ClassifierService.getProductScoresV2(1000, vertical, fsns)
    print "Got products for trendId: " + trendId
    products_ = [product[0] for product in products]
    print "Returning "+ str(fsns)+ "for trend "+trendId
    requests.post(SETU_MACHINE_IP + "api/qc", json={"trendId": trendId, "fsns": products_})


class index:
    def POST(self):
        args = json.loads(web.data())
        products = ClassifierService.getProductScores(args["number"], args["vertical"], args["positiveImages"],
                                                      args["negativeImages"])
        images = NetworkHandler.getImages([product[0] for product in products])
        render = web.template.render('/Users/anat.simran/flipkart/repos/Foobar/src/Classifier/templates/')
        return render.index(images)


class v3:
    def POST(self):
        args = json.loads(web.data())
        products = ClassifierService.getProductScoresV2(500, args["vertical"], args["fsn"])
        images = NetworkHandler.getImages([product[0] for product in products])
        render = web.template.render('/Users/anat.simran/flipkart/repos/Foobar/src/Classifier/templates/')
        return render.index(images)


class v2:
    def POST(self):
        args = json.loads(web.data())
        thread = Thread(target=JobScheduler, args=(args["trendId"], args["vertical"], args["fsn"]))
        thread.start()
        return "Your job has been scheduled"


class hello:
    def GET(self):
        return "Dayumn, my man"


class score:
    def GET(self):
        args = json.loads(web.data())


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
