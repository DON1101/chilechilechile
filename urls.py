from tornado.web import RedirectHandler, StaticFileHandler
from handlers.article import ArticleListHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    (r'/static/(.*)', StaticFileHandler, {"path": "media"}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/", ArticleListHandler),

    (r"/", RedirectHandler, {"url": "/articles/"}),
]
