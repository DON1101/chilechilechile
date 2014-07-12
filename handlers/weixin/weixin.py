# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from torndb import Connection
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
        to_user = xml.find("FromUserName").text
        from_user = xml.find("ToUserName").text

        response = ""

        if content.isdigit():
            category = int(content)
            # Handle Monday ~ Friday filtering
            if category >= 1 and category <= 5:
                category = settings.ARTICLE_CATEGORIES[category - 1]
                response = self.make_single_pic_response(
                    from_user,
                    to_user,
                    int(time.time()),
                    category["title"],
                    category["description"],
                    category["pic_url"],
                    category["article_url"],
                )
        elif content == u"最新":
            response = self.get_latest_article(
                from_user,
                to_user,
                int(time.time())
            )
        else:
            # Handle other filtering
            response = self.make_filtering_response(
                from_user,
                to_user,
                int(time.time()),
                content.encode("utf8")
            )

        self.write(response)
        self.flush()

    def make_filtering_response(self, from_user, to_user, timestamp, content):
        import article_filtering

        for filter_item in article_filtering.ARTICLE_FILTERING:
            if content in filter_item["keys"]:
                if filter_item["msg_type"] == "news":
                    return self.make_single_pic_response(
                        from_user,
                        to_user,
                        timestamp,
                        filter_item["title"],
                        filter_item["description"],
                        filter_item["pic_url"],
                        filter_item["article_url"],
                    )
                elif filter_item["msg_type"] == "text":
                    return self.make_text_response(
                        from_user,
                        to_user,
                        timestamp,
                        filter["content"],
                    )

    def get_latest_article(self, from_user, to_user, timestamp):
        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )
        sql = "SELECT * FROM articles ORDER BY time DESC LIMIT 1"
        article = db.query(sql)[0]
        return self.make_single_pic_response(
            from_user,
            to_user,
            timestamp,
            article["title"],
            article["profile"],
            article["picUrl"],
            "{0}/articles/details/{1}/".format(
                settings.SITE_HTTP_URL,
                article["id"]
            )
        )

    def make_text_response(self, from_user, to_user, timestamp, content):
        template = ("<xml>" +
                    "<ToUserName><![CDATA[%s]]></ToUserName>" +
                    "<FromUserName><![CDATA[%s]]></FromUserName>" +
                    "<CreateTime>%s</CreateTime>" +
                    "<MsgType><![CDATA[%s]]></MsgType>" +
                    "<Content><![CDATA[%s]]></Content>" +
                    "<FuncFlag>0</FuncFlag>" +
                    "</xml>")
        response = template % (to_user,
                               from_user,
                               timestamp,
                               "text",
                               content
                               )
        return response

    def make_single_pic_response(self,
                                 from_user,
                                 to_user,
                                 timestamp,
                                 title,
                                 description,
                                 pic_url,
                                 article_url):
        template = ("<xml>"
                    "<ToUserName><![CDATA[%s]]></ToUserName>"
                    "<FromUserName><![CDATA[%s]]></FromUserName>"
                    "<CreateTime>%s</CreateTime>"
                    "<MsgType><![CDATA[news]]></MsgType>"
                    "<ArticleCount>1</ArticleCount>"
                    "<Articles>"
                    "   <item>"
                    "       <Title><![CDATA[%s]]></Title>"
                    "       <Description><![CDATA[%s]]></Description>"
                    "       <PicUrl><![CDATA[%s]]></PicUrl>"
                    "       <Url><![CDATA[%s]]></Url>"
                    "   </item>"
                    "</Articles>"
                    "</xml>")
        response = template % (to_user,
                               from_user,
                               timestamp,
                               title,
                               description,
                               pic_url,
                               article_url
                               )
        return response
