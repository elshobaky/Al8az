"""
Request handlers for logs app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
# importing frequently used handlers
from fu import *
_ = t
# Data Models
from data_models import *

from user.data_models import LocalUser
from quiz.data_models import Quiz, Answer, Result
from game.data_models import Game


def add_log(user_id,user_name,cat,item_id,item_name,url=None,msg=None):
    if cat == 'g':
        url = '/game/%s' % item_id
        u = LocalUser.by_id(user_id)
        u.g_play += 1
        u.put()
    if cat in ['q','qtry']:
        url = '/quiz/%s' % item_id
        u = LocalUser.by_id(user_id)
        if u.q_solved and u.q_try:
            if cat == 'q':
                l = Logs.check_log(user_id, item_id, 'q')
                if not l : u.q_solved += 1
            ltry = Logs.check_log(user_id, item_id, 'qtry')
            if ltry: u.q_try += 1
        else:
            u.q_try = 1
            if cat == 'q':
                l = Logs.check_log(user_id, item_id, 'q')
                if not l : u.q_solved += 1
            else:
                ltry = Logs.check_log(user_id, item_id, 'qtry')
                if ltry: u.q_try += 1
        u.put()
    log = Logs.add_log(user_id,user_name,cat,item_id,item_name,url,msg)
    log.put()
    return


class GetLog(MainHandler):
    """get user logs"""
    def get(self):
        uid = self.request.get('uid')
        if uid:
            uid = int(uid)
        if not uid:
            uid = self.user.key.id()
        s = self.request.get('s')
        if not s :
            s = '0'
        n = self.request.get('n')
        if not n:
            n = '20'
        if int(n) > 50 :
            n = '50'
        self.response.headers['Content-Type'] = 'application/json'
        logs , count , current = Logs.get_log(uid,int(s),int(n))
        data = {'logs':logs, 'count':count, 'current':current}
        self.write(json.dumps(data))
