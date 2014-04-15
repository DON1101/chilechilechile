from tornado.web import RequestHandler
from lxml import etree
import settings
import hashlib
import time
import logging
logger = logging.getLogger("transformers." + __name__)


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
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        textTpl = "<xml>\n\
                    <ToUserName><![CDATA[%s]]></ToUserName>\n\
                    <FromUserName><![CDATA[%s]]></FromUserName>\n\
                    <CreateTime>%s</CreateTime>\n\
                    <MsgType><![CDATA[%s]]></MsgType>\n\
                    <Content><![CDATA[%s]]></Content>\n\
                    <FuncFlag>0</FuncFlag>\n\
                   </xml>"
        response = textTpl % (fromUser,
                              toUser,
                              int(time.time()),
                              "text",
                              content
                              )
        self.write(response)
        self.flush()
