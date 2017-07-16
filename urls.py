"""
url mapping for OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""

# import app engine frameworks
import webapp2
from webapp2_extras import routes
# import app settings
from settings import *

#import project modules /apps and request handlers
from fu import *
from home import *
from social_apis import SocialCount
# Mapping
_u = URLS_PREFIX
urls = [
    webapp2.Route(_u+'/', MainPage, 'home-page'),
    webapp2.Route(_u+'/ajax/getstars', GetStars, 'get-stars'),
    webapp2.Route(_u+'/ajax/socialcount', SocialCount),
    webapp2.Route(_u+'/switch-lang', Locale, 'language-switsh'),
    webapp2.Route(_u+'/rss', RSS, 'rss'),
    webapp2.Route('/rss.xml', RSS, 'rss-xml'),
    webapp2.Route('/games/rss', GameRSS, 'game-rss'),
    webapp2.Route('/games/rss.xml', GameRSS, 'gamee-rss-xml'),
    webapp2.Route('/search', Search, 'search'),
    webapp2.Route('/up', UP, 'update'),
]

# importing project apps urls
from lib import user
# importing urls from each app
from user import urls as users_urls
from files import urls as files_urls
from game import urls as game_urls
from quiz import urls as quiz_urls
from logs import urls as logs_urls
from admin import urls as admin_urls


urls += users_urls.urls
urls += files_urls.urls
urls += game_urls.urls
urls += quiz_urls.urls
urls += logs_urls.urls
urls += admin_urls.urls

# rendring urls
app = webapp2.WSGIApplication(urls,
	config=INTERNATIONAL_CFG, debug=DEBUG)