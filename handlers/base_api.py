from tornado.escape import json_encode
import logging
logger = logging.getLogger('transformers.' + __name__)

from handlers.base import BaseHandler


class ApiBaseHandler(BaseHandler):
    """
    Return Json as response. Work as an RESTful API handler.
    """

    ######################
    # Override Functions #
    ######################

    def generate_content(self, response):
        return response

    def generate_post_content(self, response):
        return response

    def render(self, template_name, **kwargs):
        self.write(json_encode(kwargs["kwargs"]))

    def check_xsrf_cookie(self):
        pass

    def get_argument(self, name, default=[], strip=True):
        return super(ApiBaseHandler, self).get_argument(
            name, default, strip
        ).decode("utf8").encode("utf8")
