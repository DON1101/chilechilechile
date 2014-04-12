from tornado.web import RedirectHandler, StaticFileHandler
from handlers.hello_world import HelloWorldHandler

url_patterns = [
    (r"/", HelloWorldHandler),
]
