"""
Database Models for quiz app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
import random, hashlib, datetime, logging, json
# importing google ndb datastor api
from google.appengine.ext import ndb
# user login
from google.appengine.api import users
# base ndb class
from data_model import *

class Answer(ndb.Model):
    no = ndb.IntegerProperty(required=True)
    text = ndb.StringProperty(required=True)
    true_a = ndb.BooleanProperty(default=False)


def quiz_key(group = 'default'):
    return generate_key(name='quiz', group=group)


class Quiz(RandomIndexedModel):
    title = ndb.StringProperty()
    details = ndb.TextProperty()
    answers = ndb.StructuredProperty(Answer, repeated=True)
    explain = ndb.TextProperty()
    status = ndb.IntegerProperty(default=0)
    level = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    cat = ndb.StringProperty()

    own_key_name = 'quiz'
    dict_include = None
    dict_exclude = []

    @classmethod
    def by_id(cls, qid):
        return cls.get_by_id(qid, parent = quiz_key())

    @classmethod
    def rss(cls, s=0, n=50):
        return cls.query().filter(cls.status == 1).order(-cls.created).fetch(n,offset=s)

    @classmethod
    def not_verified(cls, n=50):
        return cls.query().filter(cls.status == 0).order(-cls.created).fetch(n)
        

    @classmethod
    def register(cls,   
                 details,  
                 answers,
                 title = None,
                 explain = None,
                 level = 1):
        return cls(parent = quiz_key(),
                    title = title,
                    details = details,
                    answers = answers,
                    explain = explain,
                    level = 1)


def result_key(group = 'default'):
    return generate_key(name='result', group=group)



class Result(BaseNDB):
    user_id = ndb.IntegerProperty()
    user_name = ndb.StringProperty()
    q_no = ndb.IntegerProperty()
    true_q = ndb.IntegerProperty()
    qlist = ndb.StringProperty(repeated=True)
    result = ndb.StringProperty()

    own_key_name = 'result'
    dict_include = None
    dict_exclude = []

    @classmethod
    def by_id(cls, rid):
        return cls.get_by_id(rid, parent = result_key())

    @classmethod
    def register(cls,   
                 user_name,  
                 q_no,
                 true_q,
                 qlist,
                 result,
                 user_id=None):
        return cls(parent = result_key(),
                    user_name = user_name,
                    user_id = user_id,
                    q_no = q_no,
                    qlist = qlist,
                    result = result,
                    true_q = true_q)