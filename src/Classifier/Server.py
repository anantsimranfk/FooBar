import web
import json
import ClassifierService
import NetworkHandler
import cv

urls = (
    '/similarImages', 'index',
    '/hello', 'hello'
)


class index:
    def GET(self):
        return "Fuck off Devendra"

    def POST(self):
        args = json.loads(web.data())
        products = ClassifierService.getProductScores(args["number"], args["vertical"], args["trainedImages"],args["cosine"])
        images = NetworkHandler.getImages([product[0] for product in products])
        render = web.template.render('/Users/devendra.mandan/Desktop/Foobar/src/Classifier/templates/')
        return render.index(images)


class hello:
    def GET(self):
        return "Dayumn, my man"


class score:
    def GET(self):
        args = json.loads(web.data())


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
