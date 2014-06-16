from tornado.web import RedirectHandler, StaticFileHandler
from handlers.web.article import ArticleListHandler, ArticleDetailsHandler
from handlers.weixin import WeixinHandler
from handlers.web.proxy import ProxyHandler
from handlers.web.simple_template import SimpleTemplateHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    (r"/weixin/?$", WeixinHandler),
    (r"/articles/list/?$", ArticleListHandler),
    (r"/articles/details/(?P<article_id>\w+)/?$", ArticleDetailsHandler),
    (r"/articles/upload/?$", SimpleTemplateHandler,
     dict(template="article_upload.html")
     ),

    # Proxy url visitor
    (r"/proxy/?$", ProxyHandler),

    (r"/", RedirectHandler, {"url": "/articles/list/"}),
]
