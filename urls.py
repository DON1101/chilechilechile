from tornado.web import RedirectHandler, StaticFileHandler
from handlers.web import ArticleListHandler, ArticleDetailsHandler
from handlers.weixin import WeixinHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/list/?$", ArticleListHandler),
    (r"/articles/details/?$", ArticleDetailsHandler),

    (r"/", RedirectHandler, {"url": "/articles/list/"}),
]
