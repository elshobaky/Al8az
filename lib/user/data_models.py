"""
Database Models for user app apart of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
import random, hashlib, datetime, logging, json
# importing google ndb datastor api
from google.appengine.ext import ndb
# user login
from google.appengine.api import users
# project settings
from settings import *
# base ndb class
from data_model import *


def users_key(group = 'default'):
    return generate_key(name='lusers', group=group)


class UserSocialContact(ndb.Model):
    f = ndb.StringProperty()
    t = ndb.StringProperty()
    g = ndb.StringProperty()
    i = ndb.StringProperty()


class LocalUser(BaseNDB):
	def calc_accuracy(self,q_solved,q_try):
		if q_solved > 0 and q_try > 0:
			return round((100-((q_try*1.0)/q_solved)*100),2)
		else:
			return 0

	user_id = ndb.StringProperty()
	role = ndb.StringProperty(default='u')
	email = ndb.StringProperty()
	pw_hash = ndb.StringProperty()
	firstname = ndb.StringProperty()
	lastname = ndb.StringProperty()
	nickname = ndb.StringProperty()
	locale = ndb.StringProperty(default=LOCALE)
	about = ndb.TextProperty()
	country = ndb.StringProperty()
	avatar = ndb.IntegerProperty()
	score = ndb.IntegerProperty(default=0)
	todayscore = ndb.IntegerProperty(default=0)
	q_solved = ndb.IntegerProperty(default=0)
	q_try = ndb.IntegerProperty(default=1)
	g_play = ndb.IntegerProperty(default=0)
	accuracy = ndb.ComputedProperty(lambda self: self.calc_accuracy(self.q_solved,self.q_try))
	rate = ndb.IntegerProperty(default=0)
	level = ndb.ComputedProperty(lambda self:round((self.q_solved/20.0),2))
	contact = ndb.StructuredProperty(UserSocialContact)

	own_key_name = 'lusers'
	dict_include = None
	dict_exclude = ['user_id', 'role','created', 'last_modified']

	@classmethod
	def by_google_id(cls, uid):
		return cls.query().filter(cls.user_id == uid).get()

	@classmethod
	def by_email(cls, email):
		return cls.query().filter(cls.email == email).get()

	@classmethod
	def register(cls, user_id, email, nickname, role = 'u', group = 'default'):
		return cls(parent = users_key(group=group),
			       user_id = user_id,
			       email = email,
			       nickname = nickname,
			       role = role)

	@classmethod
	def signup(cls, firstname, lastname, nickname, pw_hash, email, role, group = 'default'):
		return cls(parent = users_key(group=group),
			       firstname = firstname,
			       lastname = lastname,
			       nickname = nickname,
			       pw_hash = pw_hash,
			       email = email,
			       role = role)

	@classmethod
	def login(cls, email, pw):
		u = cls.by_email(email)
		if u and valid_pw(email, pw, u.pw_hash):
			return u

	@classmethod
	def update_info(cls, locale='ar-EG'):
		return cls(locale=locale)

	@classmethod
	def update_contact(cls,user_id,f=None,t=None,g=None,i=None):
		c = UserSocialContact(f=f,t=t,g=g,i=i)
		u = cls.by_id(user_id)
		u.contact = c
		u.put()

	@classmethod
	def reset_today_score(cls):
		users = cls.query().filter(cls.todayscore > 0)
		for u in users:
			u.todayscore = 0
			u.put()

	@classmethod
	def get_stars(cls,ajax=False):
		stars = {}
		stars['prince'] = cls.query().order(-cls.level).get()
		stars['accurate'] = cls.query().order(-cls.accuracy).get()
		stars['today_star'] = cls.query().order(-cls.todayscore).get()
		stars['games_king'] = cls.query().order(-cls.g_play).get()
		if not ajax : return stars
		for e in stars:
			x = stars[e]
			stars[e] = stars[e].make_dict(exclude=cls.dict_exclude+['contact','about','email'])
			stars[e]['avatar'] = str(x.avatar)
		return json.dumps(stars)
            

# data models for user logs
def logs_key(group = 'default'):
    return generate_key(name='logs', group=group)

class Logs(BaseNDB):
    user_id = ndb.IntegerProperty(required=True)
    user_name = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    cat = ndb.StringProperty()
    item_id = ndb.IntegerProperty()
    item_name = ndb.StringProperty()
    url = ndb.StringProperty()
    msg = ndb.StringProperty()

    own_key_name = 'logs'
    dict_include = None
    dict_exclude = ['user_id', 'role','created', 'last_modified']
	

    @classmethod
    def add_log(cls,user_id,user_name,cat,item_id,item_name,url=None,msg=None):
        return cls(parent = logs_key(group=user_id),
                   user_id = user_id,
                   user_name = user_name,
                   cat = cat,
                   item_id = item_id,
                   item_name = item_name,
                   url = url,
                   msg = msg)

    @classmethod
    def get_log(cls,uid, s=0, n=20):
        logs = cls.query(ancestor=logs_key(group=uid)).order(-cls.created).fetch(n,offset=s)
        current = s+n
        count = cls.query().count()
        return gql_json_parser(logs), count, current

    @classmethod
    def check_log(cls,uid,item_id,cat):
        l = cls.query(ancestor=logs_key(group=uid)).filter(cls.item_id==item_id, cls.cat==cat).get()
        if l :
            return True
        return False


# old users for updting

def old_users_key(group = 'default'):
    return ndb.Key('users', group)

class User(ndb.Model):
    def calc_accuracy(self,q_solved,q_try):
        if q_solved > 0 and q_try > 0:
            return round((100-((q_try*1.0)/q_solved)*100),2)
        else:
            return 0

    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    name = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    about = ndb.TextProperty()
    country = ndb.StringProperty()
    avatar = ndb.BlobKeyProperty()
    score = ndb.IntegerProperty(default=0)
    todayscore = ndb.IntegerProperty(default=0)
    q_solved = ndb.IntegerProperty(default=0)
    q_try = ndb.IntegerProperty(default=1)
    g_play = ndb.IntegerProperty(default=0)
    accuracy = ndb.ComputedProperty(lambda self: self.calc_accuracy(self.q_solved,self.q_try))
    rate = ndb.IntegerProperty(default=0)
    level = ndb.ComputedProperty(lambda self:round((self.q_solved/20.0),2))
    contact = ndb.StructuredProperty(UserSocialContact)
    role = ndb.StringProperty(default='user')

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = old_users_key())

    @classmethod
    def by_email(cls, email):
        e = cls.query().filter(cls.email == email).get()
        return e

    @classmethod
    def register(cls,
                 firstname,
                 lastname,  
                 name, 
                 pw,  
                 email):
        pw_hash = make_pw_hash(email, pw)
        return cls(parent = old_users_key(),
                    firstname = firstname,
                    lastname = lastname,
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def update_contact(cls,user_id,f=None,t=None,g=None,i=None):
        c = UserSocialContact(f=f,t=t,g=g,i=i)
        u = cls.by_id(user_id)
        u.contact = c
        u.put()

    @classmethod
    def login(cls, email, pw):
        u = cls.by_email(email)
        if u and valid_pw(email, pw, u.pw_hash):
            return u

    @classmethod
    def reset_today_score(cls):
        users = cls.query().filter(cls.todayscore > 0)
        for u in users:
            u.todayscore = 0
            u.put()

    @classmethod
    def get_stars(cls,ajax=False):
        stars = {}
        stars['prince'] = cls.query().order(-cls.level).get()
        stars['accurate'] = cls.query().order(-cls.accuracy).get()
        stars['today_star'] = cls.query().order(-cls.todayscore).get()
        stars['games_king'] = cls.query().order(-cls.g_play).get()
        if not ajax : return stars
        for e in stars:
            x = stars[e]
            stars[e] = stars[e].to_dict(exclude=['pw_hash','contact','about','email'])
            stars[e]['id'] = x.key.id()
            stars[e]['avatar'] = str(x.avatar)
        return json.dumps(stars)