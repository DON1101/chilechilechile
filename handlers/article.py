from torndb import Connection
from tornado.web import RequestHandler
import settings
import logging
logger = logging.getLogger("transformers." + __name__)


class ArticleListHandler(RequestHandler):
    def get(self):
        template_name = "article_list.html"
        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD)
        day = self.get_argument("day", "")
        articles = db.query("SELECT * FROM articles")
        kwargs = dict(articles=articles)
        super(HelloWorldHandler, self).render(
            template_name,
            **kwargs
        )
