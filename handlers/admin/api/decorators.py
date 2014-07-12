import settings
import logging


logger = logging.getLogger("chilechilechile." + __name__)


def admin_required(func):
    """
    Administrator permission required.
    1st parameter is tornado.web.RequestHandler
    """
    def inner(*args, **kwargs):
        request = args[0]
        token = request.get_argument("token", None)
        if token == settings.ADMIN_TOKEN:
            return func(*args, **kwargs)
        else:
            request.render("", kwargs={})

    return inner
