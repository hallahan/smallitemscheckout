import os
import cgi
import datetime
import urllib
import logging
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
  email = db.EmailProperty()
  phone = db.PhoneNumberProperty()
  notes = db.TextProperty()

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



class ListClientsPage(webapp.RequestHandler):
  def get(self):
    #addSampleClients()
    clients = db.GqlQuery("SELECT * FROM Client ORDER BY last_name, first_name")
    template_values = { 'clients': clients }
    path = os.path.join(os.path.dirname(__file__), 'listclients.html')
    self.response.out.write(template.render(path, template_values))

class ListItemsPage(webapp.RequestHandler):
  def get(self):
    #addSampleItems()
    items = db.GqlQuery("SELECT * FROM Item ORDER BY name")
    template_values = { 'items': items }
    path = os.path.join(os.path.dirname(__file__), 'listitems.html')
    self.response.out.write(template.render(path, template_values))

class AddClientPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'addclient.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    firstName = self.request.get('first_name')
    lastName = self.request.get('last_name')
    psuId = self.request.get('psu_id')
    email = self.request.get('email')
    phone = self.request.get('phone')
    notes = self.request.get('notes')

    newClient = Client()
    newClient.first_name = firstName
    newClient.last_name = lastName
    newClient.psu_id = psuId
    newClient.email = email
    newClient.phone = phone
    newClient.notes = notes + "(stub)"

    newClient.put()

    self.redirect('/listclients')

class AddItemPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'additem.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    name = self.request.get('name')
    desc = self.request.get('description')

    ni = Item()
    ni.name = name
    ni.description = desc
    ni.put()

    self.redirect('/listitems')

class DeleteItemPage(webapp.RequestHandler):
  def get(self):
    raw_id = self.request.get('id')
    id = int(raw_id)
    item = Item.get_by_id(id)
    item.delete()
    self.redirect('/listitems')

class EditItemPage(webapp.RequestHandler):
  
  def get(self):
    raw_id = self.request.get('id')
    item_id = int(raw_id)
    item = Item.get_by_id(item_id)
    
    template_values = {'item' : item }
    path = os.path.join(os.path.dirname(__file__), 'edititem.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    name = self.request.get('name')
    desc = self.request.get('description')

    raw_id = self.request.get('id')
    logging.info('raw_id of item for post: ' + raw_id)
    item_id = int(raw_id)
    item = Item.get_by_id(item_id)

    item.name = name
    item.description = desc
    item.put()

    self.redirect('/listitems')
    

class EditClientPage(webapp.RequestHandler):
  
  def get(self):
    raw_id = self.request.get('id')
    logging.info('raw_id:' + raw_id)
    self.raw_id = raw_id
    logging.info('self.raw_id' + self.raw_id)
    cid = int(raw_id)
    client = Client.get_by_id(cid)
       
    template_values = {'client' : client }
    path = os.path.join(os.path.dirname(__file__), 'editclient.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    fn = self.request.get('first_name')
    ln = self.request.get('last_name')
    pi = self.request.get('psu_id')
    e = self.request.get('email')
    p = self.request.get('phone')
    n = self.request.get('notes')
    cid = self.request.get('id')
    logging.info('cid from request:'+ cid)

    #raw_id = self.request.get('id')
    #logging.info('in def post(self)')
    #logging.info('self.raw_id:' + self.raw_id)
    #logging.info('raw_id:' + raw_id)

    #cid = int(self.raw_id)
    client = Client.get_by_id(cid)

    logging.info('client name:' + client.first_name)
    logging.info('retrieved cid:' + str(client.id))

    client.first_name = fn
    client.last_name = ln
    client.psu_id = pi
    client.email = e
    client.phone = p
    client.notes = n

    client.put()

    self.redirect('/listclients')
    

class DeleteClientAction(webapp.RequestHandler):
  def get(self):
    raw_id = self.request.get('id')
    id = int(raw_id)
    client = Client.get_by_id(id)
    client.delete()
    self.redirect('/listclients')
     

class MainHandler(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


URLS = (
    ('/', MainHandler),
    ('/listclients', ListClientsPage),
    ('/listitems', ListItemsPage),
    ('/addclient', AddClientPage),
    ('/additem', AddItemPage),
    ('/deleteitem', DeleteItemPage),
    ('/deleteclient', DeleteClientAction),
    ('/edititem', EditItemPage),
    ('/editclient', EditClientPage))
def main():
    application = webapp.WSGIApplication(URLS,
                                         debug=True)
    util.run_wsgi_app(application)

    

if __name__ == '__main__':
    main()




#TEST CODE
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

def addSampleItems():
  s = Item()
  s.name = 'Item A'
  s.description = 'Item a is an item that is the first item. That is why we call it item A.'

  t = Item()
  t.name = 'Item B'
  t.description = 'Item B is an item that is the second item. That is why we call it item B.'
  s.put()
  t.put()

