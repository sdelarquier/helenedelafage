import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users


# ********************************************
# Set jinja2 template environment
# ********************************************
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


# ********************************************
# Data Store
# ********************************************
class WebsiteElem(db.Model):
	"""Models global site data store."""
	title = db.StringProperty()
	subtitle = db.StringProperty()
	welcome = db.TextProperty()
	email = db.EmailProperty()
	phone = db.PhoneNumberProperty()
	address = db.StringProperty()
	categories = db.ListProperty(str)


class NavElem(db.Model):
	"""Models navigation data store."""
	mode = db.StringProperty(required=True)
	pageName = db.DateTimeProperty(required=True)
	

class ImgElem(db.Model):
	"""Models navigation data store."""
	img = db.BlobProperty(default=None,required=True)


class ArtElem(db.Model):
	"""Models navigation data store."""
	title = db.StringProperty(required=True)
	date = db.StringProperty(required=True)
	mainPic = db.BlobProperty(default=None,required=True)
	thumb = db.BlobProperty(default=None,required=True)
	price = db.FloatProperty(required=True)
	dimension = db.FloatProperty(required=True)
	category = db.CategoryProperty(required=True)
	closeUps = db.ReferenceProperty(ImgElem)


# ********************************************
# index.html
# ********************************************
class MainPage(webapp2.RequestHandler):
	def get(self):
		adminOpt = WebsiteElem.get_or_insert('admin')
		title = adminOpt.title
		subtitle = adminOpt.subtitle
		welcome = adminOpt.welcome
		phone = adminOpt.phone
		email = adminOpt.email
		address = adminOpt.address
		
		admin_url = None
		admin_linktext = None
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			if users.is_current_user_admin():
				admin_url = '/admin'
				admin_linktext = 'Admin'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		categories = ['Meubles','Toiles','Bois']
		mode = 'welcome'
		pageName = None
		
		template_values = {
			'title': title,
			'subtitle': subtitle,
			'categories': categories,
			'mode': mode,
			'pageName': pageName,
			'welcome': welcome,
			'phone': phone,
			'email': email,	
			'address': address,
			'admin_url': admin_url,
			'admin_linktext': admin_linktext,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))


# ********************************************
# admin.html
# ********************************************
class AdminPage(webapp2.RequestHandler):
    def get(self):
		adminOpt = WebsiteElem.get_or_insert('admin')
		title = adminOpt.title
		subtitle = adminOpt.subtitle
		welcome = adminOpt.welcome
		phone = adminOpt.phone
		email = adminOpt.email
		address = adminOpt.address
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		template_values = {
			'title': title,
			'subtitle': subtitle,
			'welcome': welcome,
			'phone': phone,
			'email': email,
			'address': address,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = jinja_environment.get_template('admin.html')
		self.response.out.write(template.render(template_values))


class AdminUpdate(webapp2.RequestHandler):
	def post(self):
		adminOpt = WebsiteElem.get_or_insert('admin')
		
		adminOpt.title = self.request.get('title')
		adminOpt.subtitle = self.request.get('subtitle')
		adminOpt.welcome = self.request.get('welcome')
		adminOpt.phone = self.request.get('tel')
		adminOpt.email = self.request.get('email')
		adminOpt.address = self.request.get('address')
		
		adminOpt.put()
		self.redirect('/admin')


# ********************************************
# admin_art.html
# ********************************************
class AdminPage(webapp2.RequestHandler):
    def get(self):
    	artlib = ArtElem.all()
		
		template = jinja_environment.get_template('admin_art.html')
		self.response.out.write(template.render(template_values))


# ********************************************
# Start app engine
# ********************************************
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/admin', AdminPage),
                               ('/admin/art', AdminArtPage),
                               ('/admin/update', AdminUpdate)],
                              debug=True)