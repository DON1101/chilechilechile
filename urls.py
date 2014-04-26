from tornado.web import RedirectHandler, StaticFileHandler
import settings
from handlers.article import ArticleListHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),
    (r'/static/(.*)', StaticFileHandler, {"path": settings.static_path}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/", ArticleListHandler),

    (r"/", RedirectHandler, {"url": "/articles/"}),
]
