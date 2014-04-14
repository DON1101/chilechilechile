from tornado.web import RedirectHandler, StaticFileHandler
from handlers.hello_world import HelloWorldHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    (r"/", WeixinHandler),
]
