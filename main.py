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
from google.appengine.ext.webapp import util

class Client(db.Model):
  first_name =  db.StringProperty()
  last_name = db.StringProperty()
  psu_id = db.StringProperty()
  email = db.StringProperty()
  phone = db.StringProperty()
  notes = db.StringProperty()

def addSampleClients():
  s = Client()
  s.first_name = 'Bob'
  s.last_name = 'Palmieri'
  s.psu_id = '945-564-529'
  s.email = 'palmieri@pdx.edu'
  s.phone = '503-444-5466'
  s.notes = 'This is the first test client added to the database'

  t = Client()
  t.first_name = 'Laura'
  t.last_name = 'Holloway'
  t.psu_id = '933-243-543'
  t.email = 'hollowell@pdx.edu'
  t.phone = '503-309-3274'
  t.notes = 'This is the second test client added to the database'

  s.put()
  t.put()

class Item(db.Model):
  name = db.StringProperty()
  description = db.TextProperty()

#class Checkout(db.Model):
  #client = db.ReferenceProperty(Client)
  #items = db.ListProperty(db.Key)

  #returned = db.BooleanProperty()
  #checkout_time = DateTimeProperty(auto_now_add=True)
  #return_time = DateTimeProperty()

  #notes = db.TextProperty()


class Database:
  def getAllClients(self):
    return db.GqlQuery("SELECT * FROM Client ORDER BY last_name, first_name")

class ListClientsPage(webapp.RequestHandler):
  def get(self):
    addSampleClients()

    clients = Database().getAllClients()

    template_values = { 'clients': clients }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
  

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


def main():
    application = webapp.WSGIApplication([('/', ListClientsPage)],
                                         debug=True)
    util.run_wsgi_app(application)

    

if __name__ == '__main__':
    main()
