from tornado.web import RequestHandler
import logging
logger = logging.getLogger("transformers." + __name__)


class HelloWorldHandler(RequestHandler):
    def get(self):
        template_name = "hello_world.html"
        super(HelloWorldHandler, self).render(template_name)
