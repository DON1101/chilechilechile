from torndb import Connection
from tornado.web import RequestHandler
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)


class HelloWorldHandler(RequestHandler):
    def get(self):
        template_name = "hello_world.html"
        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD)
        articles = db.query("SELECT * FROM articles")
        kwargs = dict(articles=articles)
        super(HelloWorldHandler, self).render(
            template_name,
            **kwargs
        )
