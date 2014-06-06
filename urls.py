from tornado.web import RedirectHandler, StaticFileHandler
from handlers.web.article import ArticleListHandler, ArticleDetailsHandler
from handlers.weixin import WeixinHandler
from handlers.web.proxy import ProxyHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/list/?$", ArticleListHandler),
    (r"/articles/details/?$", ArticleDetailsHandler),

    # Proxy url visitor
    (r"/proxy/?$", ProxyHandler),

    (r"/", RedirectHandler, {"url": "/articles/list/"}),
]
