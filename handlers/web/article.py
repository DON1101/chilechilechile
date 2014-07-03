import datetime
import math
import urllib
from torndb import Connection
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base import BaseHandler


class ArticleListHandler(BaseHandler):
    def get(self):
        # template_name = "article_list.html"
        template_name = "mobile/article_list.html"
        category = self.get_argument("category", "all")
        cur_page = self.get_argument("page", "0")
        query = self.get_argument("query", "")
        num_per_page = 5

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        condition = "WHERE category='{0}'".format(category)
        if category == "all":
            condition = ""
        if query:
            condition = """WHERE UPPER(title) LIKE '%%{0}%%'
                           OR UPPER(profile) LIKE '%%{0}%%'
                           OR UPPER(author) LIKE '%%{0}%%'
                           OR UPPER(content) LIKE '%%{0}%%'
                        """.format(query.upper())

        sql = "SELECT COUNT(*) FROM articles {0}".format(condition)
        count = db.query(sql)[0]["COUNT(*)"]
        max_page = int(math.ceil((count + 0.0) / num_per_page))

        kwargs = dict(
            category=category,
            query=query,
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
    def get(self, article_id):
        # template_name = "article_details.html"
        template_name = "mobile/article_details.html"

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        sql = "SELECT * FROM articles WHERE id='{0}'".format(
            article_id)
        article = db.query(sql)[0]

        # article["read_count"], article["comment_count"] = \
        #     get_article_statistics(db, article_id)
        article["url"] = urllib.quote(article["url"])

        # Update article read count
        now = datetime.datetime.now()
        sql = """INSERT INTO article_reads (`article_id`, `user_id`, `time`)
                 VALUES ('{0}', '{1}', '{2}')
              """.format(article_id, 0, now)
        db.execute(sql)

        kwargs = dict(article=article,
                      day=article["day"])

        super(ArticleDetailsHandler, self).render(
            template_name,
            **kwargs
        )


def get_article_statistics(db_conn, article_id):
    # sql = """SELECT COUNT(*) FROM article_likes WHERE article_id='{0}'
    #       """.format(article_id)
    # like_count = db_conn.query(sql)[0]["COUNT(*)"]

    sql = """SELECT COUNT(*) FROM article_reads WHERE article_id='{0}'
          """.format(article_id)
    read_count = db_conn.query(sql)[0]["COUNT(*)"]

    sql = """SELECT COUNT(*) FROM article_comment WHERE article_id='{0}'
          """.format(article_id)
    comment_count = db_conn.query(sql)[0]["COUNT(*)"]

    return (read_count, comment_count)
