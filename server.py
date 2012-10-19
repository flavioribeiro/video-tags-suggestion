import tornado.ioloop
import tornado.web

from proportion_calculator import api_get_tags, api_get_merged_tags

class TagsHandler(tornado.web.RequestHandler):
    def get(self, term):
        self.content_type = 'application/json'
        tags = api_get_tags(term)
        self.write(tags)

class SuggestHandler(tornado.web.RequestHandler):
    def post(self, *args):
        text = self.get_argument('text')
        tags = api_get_merged_tags(text)
        if len(tags) > 10:
            for i in range(10):
                self.write(str(tags[i]))
                self.write("\n")
        else:
            for tag in tags:
                self.write(str(tag))
                self.write("\n")

application = tornado.web.Application([
    (r"/tags/(.*)", TagsHandler),
    (r"/suggest/?", SuggestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
