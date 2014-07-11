from torndb import Connection
import settings
import logging
logger = logging.getLogger("chilechilechile." + __name__)

from handlers.base_api import ApiBaseHandler
from utils.lib import convert_to_time_zone


class AdminCommentListHandler(ApiBaseHandler):
    def get(self):

        db = Connection(settings.DATABASE_SERVER,
                        settings.DATABASE_NAME,
                        settings.DATABASE_USER,
                        settings.DATABASE_PASSWORD,
                        )

        condition = """WHERE target_user_id='1' and consumed='0'
                        and article_comment.user_id=user.id"""

        sql = """SELECT *,name as user_name,time FROM article_comment,user {0}
                 ORDER BY time DESC;""".format(condition)
        comments = db.query(sql)

        for comment in comments:
            comment["time"] = convert_to_time_zone(comment["time"],
                                                   "Asia/Shanghai")
            comment["time"] = comment["time"].strftime("%Y-%m-%d %H:%M:%S")

        kwargs = dict(comments=comments,
                      )

        self.render("", kwargs=kwargs)
