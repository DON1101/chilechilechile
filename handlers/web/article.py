import math
from torndb import Connection
from tornado import gen
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)


class ArticleListHandler(RequestHandler):
    def get(self):
        template_name = "article_list.html"
        day = self.get_argument("day", "Mon")
        cur_page = self.get_argument("page", "0")
        num_per_page = 5

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        sql = "SELECT COUNT(*) FROM articles WHERE day='{0}';".format(day)
        count = db.query(sql)[0]["COUNT(*)"]
        max_page = int(math.ceil((count + 0.0) / num_per_page))

        sql = """SELECT * FROM articles WHERE day='{0}' ORDER BY time DESC
                 LIMIT {1}, {2}
              """.format(day, int(cur_page) * num_per_page, num_per_page)
        articles = db.query(sql)
        kwargs = dict(articles=articles,
                      day=day,
                      cur_page=cur_page,
                      max_page=max_page)

        super(ArticleListHandler, self).render(
            template_name,
            **kwargs
        )


class ArticleDetailsHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        template_name = "article_details.html"
        article_id = self.get_argument("id", "")

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        sql = "SELECT title, url FROM articles WHERE id='{0}'".format(
            article_id)
        article = db.query(sql)[0]

        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(article["url"])
        article_content_html = response.body

        kwargs = dict(article=article,
                      article_content_html=article_content_html)

        super(ArticleDetailsHandler, self).render(
            template_name,
            **kwargs
        )
