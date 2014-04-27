from tornado.web import RedirectHandler, StaticFileHandler
from handlers.article import ArticleListHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/", ArticleListHandler),

    (r"/", RedirectHandler, {"url": "/articles/"}),
]
