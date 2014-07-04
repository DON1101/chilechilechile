import urllib
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import logging
import settings
from handlers.base import BaseHandler


logger = logging.getLogger("chilechilechile." + __name__)


class ProxyHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        url = urllib.unquote(self.get_argument("url", ""))

        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(url)
        body = response.body.replace(
            "document.domain = \"qq.com\"",
            "document.domain = \"{0}\"".format(settings.SITE_DOMAIN),
        )
        body += """
            <script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
            <script type="text/javascript">
            $("img").each(function(){
                if(typeof $(this).attr("src") === "undefined" || $(this).attr("src").indexOf("/") == 0)
                    return;
                $(this).attr("src", "/image-proxy/?url=" + $(this).attr("src"));
            });
            $(".inner_pc_code").remove();
            </script>
        """

        kwargs = dict(body_html=body)
        super(ProxyHandler, self).render(
            "proxy/article_content.html",
            **kwargs
        )
