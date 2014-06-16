import datetime
import math
import urllib
from torndb import Connection
from tornado import gen
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base import BaseHandler


class ArticleListHandler(BaseHandler):
    def get(self):
        template_name = "article_list.html"
        day = self.get_argument("day", "all")
        cur_page = self.get_argument("page", 0)
        num_per_page = 5

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        condition = "WHERE day='{0}'".format(day)
        if day == "all":
            condition = ""

        sql = "SELECT COUNT(*) FROM articles {0}".format(condition)
        count = db.query(sql)[0]["COUNT(*)"]
        max_page = int(math.ceil((count + 0.0) / num_per_page))

        sql = """SELECT * FROM articles {0} ORDER BY time DESC
                 LIMIT {1}, {2}
              """.format(condition, int(cur_page) * num_per_page, num_per_page)
        articles = db.query(sql)

        for art in articles:
            art["read_count"], art["like_count"] = \
                get_article_statistics(db, art["id"])

        kwargs = dict(articles=articles,
                      day=day,
                      cur_page=int(cur_page),
                      max_page=max_page)

        self.render(template_name, **kwargs)

    def post(self):
        title = self.get_argument("title", "")
        author = self.get_argument("author", "")
        category = self.get_argument("category", "")
        date = self.get_argument("date", "")
        profile = self.get_argument("profile", "")
        picUrl = self.get_argument("picUrl", "")
        url = self.get_argument("url", "")

        time = datetime.datetime.strptime(date, "%m/%d/%Y")
        day = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }[time.weekday()]

        sql = """INSERT INTO articles (`title`, `author`, `day`, `time`, `url`, `profile`, `picUrl`, `category`)
                 VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');
              """.format(
              title,
              author,
              day,
              time,
              url,
              profile,
              picUrl,
              category
        )
        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )
        lastrowid = db.execute(sql)
        if lastrowid:
            self.redirect("/articles/details/{0}/".format(lastrowid))
        else:
            template_name = "/upload_error.html"
            self.render(template_name)


class ArticleDetailsHandler(BaseHandler):
    @gen.coroutine
    def get(self, article_id):
        template_name = "article_details.html"

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        sql = "SELECT * FROM articles WHERE id='{0}'".format(
            article_id)
        article = db.query(sql)[0]

        article["read_count"], article["like_count"] = \
            get_article_statistics(db, article_id)
        article["url"] = urllib.quote(article["url"])

        kwargs = dict(article=article,
                      day=article["day"])

        super(ArticleDetailsHandler, self).render(
            template_name,
            **kwargs
        )


def get_article_statistics(db_conn, article_id):
    sql = """SELECT COUNT(*) FROM article_likes WHERE article_id='{0}'
          """.format(article_id)
    like_count = db_conn.query(sql)[0]["COUNT(*)"]

    sql = """SELECT COUNT(*) FROM article_reads WHERE article_id='{0}'
          """.format(article_id)
    read_count = db_conn.query(sql)[0]["COUNT(*)"]

    return (read_count, like_count)
