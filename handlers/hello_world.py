from torndb import Connection
from tornado.web import RequestHandler
import logging
logger = logging.getLogger("transformers." + __name__)


class HelloWorldHandler(RequestHandler):
    def get(self):
        template_name = "hello_world.html"
        db = Connection("localhost", "chilechilechile", "root", "MS@don1988")
        articles = db.query("SELECT * FROM articles")
        kwargs = dict(articles=articles)
        super(HelloWorldHandler, self).render(
            template_name,
            **kwargs
        )
