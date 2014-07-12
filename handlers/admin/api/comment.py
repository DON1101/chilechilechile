from torndb import Connection
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.admin.api.decorators import admin_required
from handlers.base_api import ApiBaseHandler
from utils.lib import convert_to_time_zone


class AdminCommentListHandler(ApiBaseHandler):
    @admin_required
    def get(self):

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        condition = """WHERE target_user_id='1' and consumed='0'
                        and article_comment.user_id=user.id
                        and article_comment.article_id=articles.id"""

        sql = """SELECT user_id, name AS user_name, email, article_id,
                        article_comment.time AS time, title as article_title,
                        article_comment.content AS content
                 FROM article_comment,user,articles {0}
                 ORDER BY article_comment.time DESC;""".format(condition)
        comments = db.query(sql)

        for comment in comments:
            comment["time"] = convert_to_time_zone(comment["time"],
                                                   "Asia/Shanghai")
            comment["time"] = comment["time"].strftime("%Y-%m-%d %H:%M:%S")

        kwargs = dict(comments=comments,
                      )

        self.render("", kwargs=kwargs)
