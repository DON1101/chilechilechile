from tornado.web import RedirectHandler, StaticFileHandler
from handlers.web.article import ArticleListHandler, ArticleDetailsHandler
from handlers.weixin import WeixinHandler
from handlers.web.proxy import ProxyHandler
from handlers.web.image_proxy import ImageProxyHandler
from handlers.web.simple_template import SimpleTemplateHandler
from handlers.web.api.article import RestfulArticleListHandler
from handlers.web.api.comment import RestfulCommentsHandler

url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    # Weixin Client
    (r"/weixin/?$", WeixinHandler),

    # Website Desktop
    (r"/articles/list/?$", ArticleListHandler),
    (r"/articles/details/(?P<article_id>\w+)/?$", ArticleDetailsHandler),
    (r"/articles/upload/?$", SimpleTemplateHandler,
     dict(template="article_upload.html")
     ),

    # Website Mobile Phone
    (r"/m/?$", SimpleTemplateHandler,
     dict(template="mobile/index.html")
     ),
    (r"/m/left-sidebar/?$", SimpleTemplateHandler,
     dict(template="mobile/left_sidebar.html")
     ),
    (r"/m/right-sidebar/?$", SimpleTemplateHandler,
     dict(template="mobile/right_sidebar.html")
     ),
    (r"/m/info/?$", SimpleTemplateHandler,
     dict(template="mobile/info.html")
     ),

    # Proxy url visitor
    (r"/proxy/?$", ProxyHandler),
    (r"/image-proxy/?$", ImageProxyHandler),

    # RESTful API
    (r"/api/articles/list/?$", RestfulArticleListHandler),
    (r"/api/articles/comments/(?P<article_id>\w+)/?$", RestfulCommentsHandler),

    (r"/", RedirectHandler, {"url": "/articles/list/"}),
]
