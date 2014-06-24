import urllib2
import settings
import traceback
import time
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
                if not article["content"]:
                    generate_article_content(article["id"])
            print "All article updated!"
        except Exception as err:
            track = traceback.format_exc()
            print "{0}: {1}".format(err, track)


def generate_article_content(article_id):
    sql = "SELECT * FROM articles WHERE id='{0}'".format(article_id)
    article = db.query(sql)[0]
    article_url = article["url"]
    article_content = urllib2.urlopen(article_url).read()

    sql = "UPDATE articles SET content=%s WHERE id=%s"
    db.execute(sql, article_content, article_id)
    print "Updated article {0} successfully.".format(article_id)

    # time.sleep(1)
