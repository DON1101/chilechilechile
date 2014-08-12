# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from torndb import Connection
from lxml import etree
import settings
import hashlib
import time
import logging
from handlers.weixin import article_filtering


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
        search_prefix = u"吃"

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
        elif content.startswith(search_prefix + u"：") or \
                content.startswith(search_prefix + u":"):
            # Handle query search
            if content.startswith(search_prefix + u"："):
                query = content.replace(search_prefix + u"：", "")
            elif content.startswith(search_prefix + u":"):
                query = content.replace(search_prefix + u":", "")
            response = self.search_for_articles(
                from_user,
                to_user,
                int(time.time()),
                query)
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
                        filter_item["content"],
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
            "{0}/m#/article_details/{1}".format(
                settings.SITE_HTTP_URL,
                article["id"]
            )
        )

    def search_for_articles(self, from_user, to_user, timestamp, query):
        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )
        # Simple way to avoid SQL insertion attack
        if query.strip() and ";" not in query:
            condition = """WHERE UPPER(title) LIKE '%%{0}%%'
                           OR UPPER(profile) LIKE '%%{0}%%'
                           OR UPPER(author) LIKE '%%{0}%%'
                           OR UPPER(content) LIKE '%%{0}%%'
                        """.format(query.strip().upper())
        else:
            condition = ""
        sql = "SELECT * FROM articles {0} ORDER BY time DESC LIMIT 10;".format(
            condition)
        articles = db.query(sql)
        if len(articles) > 0:
            return self.make_multi_pic_response(
                from_user,
                to_user,
                timestamp,
                [title for title in articles["title"]],
                [description for description in articles["description"]],
                [pic_url for pic_url in articles["pic_url"]],
                [article_url for article_url in articles["article_url"]])
        else:
            return self.make_text_response(
                from_user,
                to_user,
                timestamp,
                u"还没有关于“%s”的内容哦！你有什么想法呢？告诉微君吧！" % query)

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

    def make_multi_pic_response(self,
                                from_user,
                                to_user,
                                timestamp,
                                titles,
                                descriptions,
                                pic_urls,
                                article_urls):
        items_response = ""
        for i in range(len(titles)):
            title = titles[i]
            description = descriptions[i]
            pic_url = pic_urls[i]
            article_url = article_urls[i]
            items_response += ("<item>"
                               "   <Title><![CDATA[%s]]></Title>"
                               "   <Description><![CDATA[%s]]></Description>"
                               "   <PicUrl><![CDATA[%s]]></PicUrl>"
                               "   <Url><![CDATA[%s]]></Url>"
                               "</item>" % (title,
                                            description,
                                            pic_url,
                                            article_url))
        template = ("<xml>"
                    "<ToUserName><![CDATA[%s]]></ToUserName>"
                    "<FromUserName><![CDATA[%s]]></FromUserName>"
                    "<CreateTime>%s</CreateTime>"
                    "<MsgType><![CDATA[news]]></MsgType>"
                    "<ArticleCount>1</ArticleCount>"
                    "<Articles>"
                    "%s"
                    "</Articles>"
                    "</xml>")
        response = template % (to_user,
                               from_user,
                               timestamp,
                               items_response
                               )
        return response
