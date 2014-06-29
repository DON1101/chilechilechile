# -*- coding: utf-8 -*-
import logging
import tornado
import tornado.template
import os
from tornado.options import define, options

import logconfig

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
tornado.options.parse_command_line()


############################
# Deployment Configuration #
############################


class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

DEBUG = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug

if DEBUG:
    SESSION_COOKIE_DOMAIN = "127.0.0.1"
else:
    SESSION_COOKIE_DOMAIN = ""
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
COOKIE_SECRET = "your-cookie-secret"

SITE_NAME = "chilechilechile"
SITE_HTTP_URL = "http://127.0.0.1"
SITE_DOMAIN = "127.0.0.1"

####################
# DATABASE RELATED #
####################

DATABASE_SERVER = "localhost"
DATABASE_USER = "root"
DATABASE_PASSWORD = "MS@don1988"
DATABASE_NAME = "chilechilechile"

##################
# WEIXIN RELATED #
##################
WEIXIN_TOKEN = "echo_don"

##########################
# LOCAL SETTINGS RELATED #
##########################

try:
    from local_settings import *
except ImportError:
    pass

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')
STATIC_URL = '/static'

settings = {}
settings['debug'] = DEBUG
settings['static_path'] = MEDIA_ROOT
settings['xsrf_cookies'] = False
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

SYSLOG_TAG = "chilechilechile"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    'loggers': {
        'chilechilechile': {},
    },
}

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

logconfig.initialize_logging(
    SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
    LOG_LEVEL, USE_SYSLOG)

if options.config:
    tornado.options.parse_config_file(options.config)


settings['cookie_secret'] = COOKIE_SECRET


##################################
# chilechilechile related config #
##################################
ARTICLE_CATEGORIES = [
    {
        "title": "旅行食记",
        "description": "一趟旅行，就是一场味蕾的冒险。跨越七大洲，精心收藏大家旅行中的美食，有饮毛茹血的刺激原始，有最地道的巷弄庶民餐厅，也有皇宫城堡的亘古奢华……",
        "pic_url": "http://mmsns.qpic.cn/mmsns/8gATibUoyKqhz5jXSu6H4alwA9ic4V5XibzbEAY7apqm3YcfcRpwSXRicA/0",
        "article_url": SITE_HTTP_URL + "/m#/article_list/0/0",
    },
    {
        "title": "精神食粮（已暂停）",
        "description": "当浮躁成为社会的常态，什么样的精神食粮，最能安抚你的内心？一段散步，一次KTV，一本好书，一张唱片，一次长跑，一部电影……",
        "pic_url": "http://mmsns.qpic.cn/mmsns/8gATibUoyKqhz5jXSu6H4alwA9ic4V5XibzOmwicicYLIBhCQdEaS3fIwFw/0",
        "article_url": SITE_HTTP_URL + "/m#/article_list/1/0",
    },
    {
        "title": "吃情男女",
        "description": "这是鼓励你从人生争取更多的一个专栏。自由社会的现代人，日常的饮食起居所面对的选择已经多得不可收拾。选择餐厅，选择菜式，选择饮料，选择甜品……还没有包括最重要的选择，比如要不要同居？要不要结婚？要不要孩子？等等等等",
        "pic_url": "http://mmsns.qpic.cn/mmsns/8gATibUoyKqjzkI9psr3RA0n2oFvw1HUPicRlYkfuN0cUuRgeZsO8CUA/0",
        "article_url": SITE_HTTP_URL + "/m#/article_list/2/0",
    },
    {
        "title": "私房推荐",
        "description": "私宅料理，靠口耳相传。私房，又多了相亲相爱，一般人我不告诉他的意思。你最爱的那间餐厅，最想为Ta做的那道料理，具体怎么做，味道如何，是否可以与我们分享？",
        "pic_url": "http://mmsns.qpic.cn/mmsns/8gATibUoyKqhpPc5up34Nk3mUcgrt4jhzrUIdsSEYecux94y86Ugib3A/0",
        "article_url": SITE_HTTP_URL + "/m#/article_list/3/0",
    },
    {
        "title": "话题探讨（已暂停）",
        "description": "“吃”是一个十分容易拉近关系的话题！素材收集，什么样的饮食话题你最关注，请告诉微君。",
        "pic_url": "http://mmsns.qpic.cn/mmsns/8gATibUoyKqjdnsNfHvSM44u0rQaypGib6tRPTH6Fk85c8xfaNduEQGQ/0",
        "article_url": SITE_HTTP_URL + "/m#/article_list/4/0",
    },
]

ARTICLE_CATEGORY_CODES = {
    "shiji": 0,
    "jingshen": 1,
    "nannv": 2,
    "sifang": 3,
    "huati": 4,
}

DEFAULT_USER_NAME = "匿名"

try:
    from extra_settings import *
except ImportError:
    pass
