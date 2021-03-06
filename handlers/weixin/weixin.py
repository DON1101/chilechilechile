# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from torndb import Connection
from lxml import etree
import settings
import hashlib
import time
import logging
import traceback
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
        to_user = xml.find("FromUserName").text
        from_user = xml.find("ToUserName").text
        msg_type = xml.find("MsgType").text

        if msg_type == "event":
            event = xml.find("Event").text
            if event == "subscribe":
                response = self.make_subscribe_response(
                    from_user,
                    to_user,
                    int(time.time())
                )
                self.write(response)
                self.flush()
                return

        content = xml.find("Content").text

        def _get_prefix(content):
            for prefix in search_prefix_list:
                if content.startswith(prefix):
                    return prefix
            return None
        search_prefix_list = [u" ", u" ", u"\t"]
        search_prefix = _get_prefix(content)

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
        elif search_prefix is not None:
            # Handle query search
            query = content.replace(search_prefix, "")
            try:
                response = self.search_for_articles(
                    from_user,
                    to_user,
                    int(time.time()),
                    query)
            except:
                logger.error(traceback.format_exc())
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
            condition = u"""WHERE UPPER(title) LIKE '%%{0}%%'
                           OR UPPER(profile) LIKE '%%{0}%%'
                           OR UPPER(author) LIKE '%%{0}%%'
                           OR UPPER(content) LIKE '%%{0}%%'
                        """.format(query.strip().upper())
        else:
            condition = ""
        sql = u"SELECT * FROM articles {0} ORDER BY time DESC LIMIT 10".format(
            condition)
        articles = db.query(sql)
        if len(articles) > 0:
            return self.make_multi_pic_response(
                from_user,
                to_user,
                timestamp,
                [article["title"] for article in articles],
                [article["profile"] for article in articles],
                [article["picUrl"] for article in articles],
                ["{0}/m#/article_details/{1}".format(
                    settings.SITE_HTTP_URL,
                    article["id"]
                ) for article in articles])
        else:
            return self.make_text_response(
                from_user,
                to_user,
                timestamp,
                u"还没有关于“%s”的内容哦！你有什么想法呢？告诉微君吧！" % query)

    def make_subscribe_response(self, from_user, to_user, timestamp):
        content = u"""
【并非关于吃的一切】与吃有关的情，一起来分享。
回复数字“1”获取：旅行食记 系列；
回复数字“2”获取：精神食粮 系列(已暂停更新)；
回复数字“3”获取：吃情男女 系列；
回复数字“4”获取：私房推荐 系列；
回复数字“5”获取：话题探讨 系列(已暂停更新)；
回复 “最新” 获取：最新一期文章；
回复 “[空格][关键词]” 获取：搜索相应关键词的文章，比如“ 牛排”。
        """
        return self.make_text_response(
            from_user,
            to_user,
            timestamp,
            content,
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
                    "<ArticleCount>%s</ArticleCount>"
                    "<Articles>"
                    "%s"
                    "</Articles>"
                    "</xml>")
        response = template % (to_user,
                               from_user,
                               timestamp,
                               len(titles),
                               items_response
                               )
        return response
