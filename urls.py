from tornado.web import RedirectHandler
from handlers.article import ArticleListHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    (r"/weixin/?$", WeixinHandler),
    (r"/articles/", ArticleListHandler),

    (r"/", RedirectHandler, {"url": "/articles/"}),
]
