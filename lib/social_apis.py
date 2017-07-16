import json
import urllib
import tweepy
import json
import fu
MainHandler = fu.MainHandler
def get_page(url):
	try:
		page = urllib.urlopen(url).read()
	except Exception:
		page = None
	return page


def facebook():
	app_id = '1653069704912099'
	app_secret = 'c87ef7c55a5743448b751bb579657243'
	page = get_page("https://graph.facebook.com/al8azcom?fields=likes&summary=true&access_token=%s|%s"%(app_id, app_secret))
	try :
		p = json.loads(page)
		return p['likes']
	except:
		return '0000'

def googleplus():
	user = '118064797796413637139'
	key = 'AIzaSyAvGmiTNAU-MP4n5FMgfh1_0QNsr2Of4GU'
	url = 'https://www.googleapis.com/plus/v1/people/'+user+'?key='+key
	page = get_page(url)
	try:
		p = json.loads(page)
		return p["circledByCount"]
	except:
		return '0000'


def twitter():
	consumer_key='EGC2oZWvRCZB3TzyUfbrAR7ig'
	consumer_secret='PDftcmxRQ0ynbkMQM0sXOUOrLlUV0RtrhXAazQciFCaL3hdOd7'
	access_token='3019567469-zOmGRzgYjnHsuNHpIfx541Wb45DbIKoxYtbLpmJ'
	access_token_secret='OTZfCYFg0XetwBgQPTSfxIxyZft7sImH5n5s2RsX6vI3O'
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		user = api.get_user('al8azcom')
		return user.followers_count
	except:
		return '0000'
	
def get_social_counts():
    return {"f":facebook(),
            "g":googleplus(),
            "t":twitter()}


def get_social_counts_off():
    return {"f":3482,
            "g":82,
            "t":40}

class SocialCount(MainHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.write(json.dumps(get_social_counts()))

