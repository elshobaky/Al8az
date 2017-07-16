"""
url mapping for game app a part of OpenAl8az project.
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
_u = URLS_PREFIX + '/game' # you can add prefix for app ex. -u = URLS_PREFIX + '/page'
urls = [
   webapp2.Route('/admin/addgame', AddGame, 'add-game'),
   ('/admin/editgame/([0-9]+)', EditGame),
   webapp2.Route('/games', Games, 'games'),
   (_u+'/([0-9]+)', GamePerma),
]

# rendring urls
#app = webapp2.WSGIApplication(urls,
#	config=INTERNATIONAL_CFG, debug=DEBUG)
