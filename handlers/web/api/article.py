import math
from torndb import Connection
import settings
import logging
import urllib
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base_api import ApiBaseHandler


class RestfulArticleListHandler(ApiBaseHandler):
    def get(self):
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

        sql = """SELECT articles.id AS id, title, profile, author, url, picUrl,
                        articles.time AS time,
                        (SELECT COUNT(*) FROM article_reads
                         WHERE article_reads.article_id=articles.id) AS read_count,
                        (SELECT COUNT(*) FROM article_comment
                         WHERE article_comment.article_id=articles.id) AS comment_count
                 FROM articles
                 {0}
                 ORDER BY articles.time DESC
                 LIMIT {1}, {2};
              """.format(condition, int(cur_page) * num_per_page, num_per_page)
        print sql
        articles = db.query(sql)

        for art in articles:
            # art["read_count"], art["comment_count"] = \
            #     get_article_statistics(db, art["id"])
            art["time"] = art["time"].strftime("%Y-%m-%d")
            art["picUrl"] = "/image-proxy/?url={0}".format(
                urllib.quote(art["picUrl"])
            )

        kwargs = dict(articles=articles,
                      category=category,
                      cur_page=int(cur_page),
                      max_page=max_page)

        self.render("", kwargs=kwargs)


def get_article_statistics(db_conn, article_id):
    sql = """SELECT COUNT(*) FROM article_comment WHERE article_id='{0}'
          """.format(article_id)
    comment_count = db_conn.query(sql)[0]["COUNT(*)"]

    sql = """SELECT COUNT(*) FROM article_reads WHERE article_id='{0}'
          """.format(article_id)
    read_count = db_conn.query(sql)[0]["COUNT(*)"]

    return (read_count, comment_count)
