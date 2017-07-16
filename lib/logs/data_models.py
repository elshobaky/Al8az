"""
Database Models for logs app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
import random, hashlib, datetime, logging, json
# importing google ndb datastor api
from google.appengine.ext import ndb
# user login
from google.appengine.api import users
# base ndb class
from data_model import *
from fu import gql_json_parser

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
    dict_exclude = ['user_id', 'role', 'last_modified']
  

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