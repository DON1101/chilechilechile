import urllib
import logging
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base_api import ApiBaseHandler


class ImageProxyHandler(ApiBaseHandler):
    @gen.coroutine
    def get(self):
        image_url = urllib.unquote(self.get_argument("url", ""))

        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(image_url)

        self.set_header('Content-type', 'image/png')
        self.write(response.body)
