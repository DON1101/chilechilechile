import datetime
from torndb import Connection
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base_api import ApiBaseHandler
from utils.lib import convert_to_time_zone


class RestfulCommentsHandler(ApiBaseHandler):
    def get(self, article_id):

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        condition = "WHERE article_id='{0}'".format(article_id)

        sql = """SELECT * FROM article_comment {0} ORDER BY time DESC;
              """.format(condition)
        comments = db.query(sql)

        for comment in comments:
            user_id = comment["user_id"]
            sql = "SELECT * FROM user WHERE id='{0}';".format(user_id)
            user = db.query(sql)[0]

            comment["user_name"] = user["name"]
            comment["time"] = convert_to_time_zone(comment["time"],
                                                   "Asia/Shanghai")
            comment["time"] = comment["time"].strftime("%Y-%m-%d %H:%M:%S")

        kwargs = dict(comments=comments)

        self.render("", kwargs=kwargs)

    def post(self, article_id):
        user_name = self.get_argument("user_name", "")
        user_email = self.get_argument("user_email", "")
        content = self.get_argument("content", "")
        now = datetime.datetime.now()
        if not user_name:
            user_name = settings.DEFAULT_USER_NAME

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        sql = """INSERT INTO user (`name`, `email`)
                 VALUES ('{0}', '{1}');
              """.format(
              user_name,
              user_email,
        )
        user_id = db.execute(sql)

        sql = """INSERT INTO article_comment (`article_id`, `user_id`, `time`, `content`)
                 VALUES ('{0}', '{1}', '{2}', '{3}');
              """.format(
              article_id,
              user_id,
              now,
              content,
        )
        db.execute(sql)

        self.redirect("/api/articles/comments/{0}/".format(article_id))
