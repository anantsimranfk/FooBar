import web

urls = (
    '/similarImages', 'index',
    '/hello', 'hello'
)


class index:
    def GET(self):
        return "Fuck off Devendra"

class hello:
    def GET(self):
        return "Dayumn, my man"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()