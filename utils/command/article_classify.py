import datetime
import settings
import traceback
from torndb import Connection

import logging
logger = logging.getLogger("chilechilechile." + __name__)


db = Connection(settings.DATABASE_SERVER,
                settings.DATABASE_NAME,
                settings.DATABASE_USER,
                settings.DATABASE_PASSWORD,
                )


class Command():
    def handle(self):
        """
        Import modules:
            from tornado.options import define, options, parse_command_line
        Define args: define("test", default=8888, help="test help", type=int)
        Start to parse: parse_command_line()
        Get args: options["test"]
        """
        try:
            sql = "SELECT * FROM articles"
            articles = db.query(sql)
            for article in articles:
                classify(article)
            print "All article updated!"
        except Exception as err:
            track = traceback.format_exc()
            print "Article {0}: {1}: {2}".format(article["id"], err, track)


def classify(article):
    submited_at = article["time"]
    updated_time = datetime.datetime(2014, 6, 22)

    if article["day"] == "Sat":
        return

    if submited_at < updated_time:
        categories = {
            "Mon": "shiji",
            "Tue": "jingshen",
            "Wed": "nannv",
            "Thu": "sifang",
            "Fri": "huati",
        }
        sql = "UPDATE articles SET category=%s WHERE id=%s"
        category = settings.ARTICLE_CATEGORY_CODES[
            categories[article["day"]]
        ]
        db.execute(sql, category, article["id"])
        print "Updated article {0} successfully.".format(
            article["id"]
        )
