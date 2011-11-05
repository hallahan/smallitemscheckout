import os
import cgi
import datetime
import urllib
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Client(db.Model):
  first_name =  db.StringProperty()
  last_name = db.StringProperty()
  psu_id = db.StringProperty()
  email = db.EmailProperty()
  phone = db.PhoneProperty()
  notes = db.TextProperty()

class Item(db.Model):
  name = db.StringProperty()
  description = db.TextProperty()

class Checkout(db.Model):
  client = db.ReferenceProperty(Client)
  items = db.ListProperty(db.Key)

  returned = db.BooleanProperty()
  checkout_time = DateTimeProperty()
  return_time = DateTimeProperty()
  notes = db.TextProperty()
  

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
