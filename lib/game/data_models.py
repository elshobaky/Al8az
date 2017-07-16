"""
Database Models for game app apart of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
import random, hashlib, datetime, logging, json
# importing google ndb datastor api
from google.appengine.ext import ndb
# user login
from google.appengine.api import users
# base ndb class
from data_model import *


def game_key(group = 'default'):
    return generate_key(name='game', group=group)


class Game(RandomIndexedModel):
    title = ndb.StringProperty()
    details = ndb.TextProperty()
    swf = ndb.BlobKeyProperty()
    img = ndb.BlobKeyProperty()
    status = ndb.IntegerProperty(default=0)
    level = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    cat = ndb.StringProperty()
    
    own_key_name = 'game'
    dict_include = None
    dict_exclude = []

    @classmethod
    def by_id(cls, gid):
        return cls.get_by_id(gid, parent = game_key())

    @classmethod
    def get_page(cls, p=1):
        games = cls.query().filter(cls.status == 1).order(-cls.created).fetch(18,offset=(p-1)*18)
        count = cls.query().filter(cls.status == 1).count()
        return games , count

    @classmethod
    def rss(cls, s=0, n=50):
        return cls.query().filter(cls.status == 1).order(-cls.created).fetch(n,offset=s)

    @classmethod
    def not_verified(cls, n=50):
        return cls.query().filter(cls.status == 0).order(-cls.created).fetch(n)


    @classmethod
    def register(cls,   
                 title,  
                 swf,
                 img = None,
                 details=None):
        return cls(parent = game_key(),
                    title = title,
                    swf = swf,
                    img = img,
                    details = details)