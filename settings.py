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

SITE_NAME = "chilechilechile"

try:
    from extra_settings import *
except ImportError:
    pass
