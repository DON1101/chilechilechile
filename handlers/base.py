import tornado
import tornado.escape
import tornado.web

import logging
logger = logging.getLogger('chilechilechile.' + __name__)

from context_processor import site_metadata


class BaseHandler(tornado.web.RequestHandler):
    """
    A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def get_argument(self, name, default=[], strip=True):
        argument = super(BaseHandler, self).get_argument(
            name, default, strip
        )
        if argument:
            argument = argument.encode("utf8")
        return argument

    def render(self, template_name, **kwargs):
        site_meta_data = site_metadata()
        kwargs.update(site_meta_data)

        super(BaseHandler, self).render(template_name, **kwargs)
