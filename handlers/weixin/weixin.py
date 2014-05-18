from tornado.web import RequestHandler
from lxml import etree
import settings
import hashlib
import time
import logging
logger = logging.getLogger("chilechilechile." + __name__)


class WeixinHandler(RequestHandler):
    def get(self):
        # Get input parameters
        signature = self.get_argument("signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")
        # My weixin token
        token = settings.WEIXIN_TOKEN
        # Sort in dictionary order
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        # If it's a request from weixin, respond echostr
        if hashcode == signature:
            self.write(echostr)
            self.flush()

    def post(self):
        str_xml = self.request.body  # Get Post data
        xml = etree.fromstring(str_xml)  # xml parsing
        content = xml.find("Content").text
        msgType = xml.find("MsgType").text
        to_user = xml.find("FromUserName").text
        from_user = xml.find("ToUserName").text

        response = self.construct_text_response(
            from_user,
            to_user,
            int(time.time()),
            "text",
            content
        )
        self.write(response)
        self.flush()

    def construct_text_response(self, from_user, to_user, timestamp, content):
        template = ("<xml>" +
                    "<ToUserName><![CDATA[{0}]]></ToUserName>" +
                    "<FromUserName><![CDATA[{1}]]></FromUserName>" +
                    "<CreateTime>{2}</CreateTime>" +
                    "<MsgType><![CDATA[{3}]]></MsgType>" +
                    "<Content><![CDATA[{4}]]></Content>" +
                    "<FuncFlag>0</FuncFlag>" +
                    "</xml>")
        response = template.format(to_user,
                                   from_user,
                                   timestamp,
                                   "text",
                                   content
                                   )
        return response
