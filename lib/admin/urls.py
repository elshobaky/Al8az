"""
url mapping for admin app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""

# import app engine frameworks
import webapp2
from webapp2_extras import routes

# import app settings
from settings import *

#import project modules and request handlers
from request_handlers import *

#URL Mapping
# ex. [webapp2.Route(_u+'/signup', SignUp, 'user-signup'),]
_u = URLS_PREFIX + '/admin' # you can add prefix for app ex. -u = URLS_PREFIX + '/page'
urls = [
   webapp2.Route(_u, AdminHome, 'admin-home'),
   webapp2.Route(_u+'/addadmin', AddAdmin, 'add-admin'),
   webapp2.Route('/ajax/admingetcount', GetAdminCount, 'get-admin-count')
]

# rendring urls
#app = webapp2.WSGIApplication(urls,
#	config=INTERNATIONAL_CFG, debug=DEBUG)
