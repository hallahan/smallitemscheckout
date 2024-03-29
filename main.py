import os
import cgi
import urllib
import logging
import wsgiref.handlers
from datetime import datetime
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
  client_id = db.StringProperty()

class Item(db.Model):
  name = db.StringProperty()
  description = db.TextProperty()

class Checkout(db.Model):
  client = db.ReferenceProperty(reference_class=Client)
  items = db.ListProperty(db.Key)
  returned = db.BooleanProperty(default=False)
  checkout_time = db.DateTimeProperty(auto_now_add=True)
  return_time = db.DateTimeProperty()
  notes = db.TextProperty()

  itemObjs = list()

  def __init__(self):
    for item_key in self.items:
      self.itemObjs.append(db.get(item_key))

#class CheckoutItemRel(db.Model):
  #checkout = db.ReferenceProperty(Checkout)
  #item = db.ReferenceProperty(Item)
  #quantity = db.Integer(default=1)


def addSampleCheckouts():
  item1 = Item.get_by_id(39)
  item2 = Item.get_by_id(21)
  item3 = Item.get_by_id(49)
  item4 = Item.get_by_id(20)

  client1 = Client.get_by_id(5)
  client2 = Client.get_by_id(17)
  client3 = Client.get_by_id(46)

  c1 = Checkout()
  c2 = Checkout()
  c3 = Checkout()
  
  c1.client = client1
  c1.items.append(item1.key())
  c1.items.append(item2.key())
  c1.returned = False
  c1.return_time = datetime(2011,12,12,15,30)
  c1.notes = 'This is the first sample checkout.'

  c2.client = client2
  c2.items.append(item4.key())
  c2.returned = False
  c2.checkout_time = datetime(2011,11,5,8,30)
  c2.return_time = datetime(2011,11,6,16,20)
  c2.notes = 'This is the second sample checkout. It should be overdue.'

  c3.client = client3
  c3.items.append(item4.key())
  c3.items.append(item3.key())
  c3.items.append(item2.key())
  c3.items.append(item1.key())
  c3.returned = False
  c3.return_time = datetime(2011,11,9,17,22)
  c3.notes = 'This one should be due on Thursday.'

  c1.put()
  c2.put()
  c3.put()

class ListClientsPage(webapp.RequestHandler):
  def get(self):
    #addSampleClients()
    clients = db.GqlQuery("SELECT * FROM Client ORDER BY last_name, first_name")
    template_values = { 'clients': clients }
    path = os.path.join(os.path.dirname(__file__), 'listclients.html')
    self.response.out.write(template.render(path, template_values))

class CheckoutHistoryPage(webapp.RequestHandler):
  def get(self):
    addSampleCheckouts()
    checkouts = db.GqlQuery("SELECT * FROM Checkout ORDER BY checkout_time")    
  
    template_values = { 'checkouts' : checkouts }
    path = os.path.join(os.path.dirname(__file__), 'checkouthistory.html')
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
    newClient.notes = notes

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
    id_ = int(raw_id)
    client = Client.get_by_id(id_)
    client.client_id = raw_id #TODO we need to find a better way
    
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

    raw_id = self.request.get('id')
    cid = int(raw_id)
    client = Client.get_by_id(cid)

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
    ('/editclient', EditClientPage),
    ('/checkouthistory', CheckoutHistoryPage))


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

