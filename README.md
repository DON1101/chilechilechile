Basic components in Tornado framework:

- URL Mapping
  
  All the url mapping settings could be found in /urls.py
  
  For each url, there's a RequestHandler class specified. RequestHandler is the actual controller.

- RequestHandler

  All the request handlers could be found under /handlers/

  Each request handler is a subclass of tornado.web.RequestHandler. They process the HTTP request, communicate with MySql database and make correct HTTP response.

- Templates

  All the templates could be found under /templates/

  Template is the "View" part of Tornado framework. Each template is in *.html format, we can show whatever we want in the template, so that browser can view it.


How to run Tornado server?

- Setup Python environment & virtualenv

  sudo apt-get install python-setuptools python-dev libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev

  sudo easy_install pip

  sudo pip install virtualenv virtualenvwrapper ipython

- Create a virtual environment directory

  virtualenv --distribute /opt/chilechilechile

  cd /opt/chilechilechile

  source bin/activate

- Git clone repo

  git clone git@github.com:DON1101/chilechilechile.git src

- Install Python packages from file /requirements/development.txt

  pip install tornado

  pip install torndb

  pip install mysql-python

  pip install lxml

  pip install pytz

  pip install tzlocal

- Start your MySql database

- Run Tornado server

  python app.py


