"""
Request handlers for admin app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
# importing frequently used handlers
from fu import *
_ = t
# Data Models
from data_models import *
from quiz.data_models import Quiz
from game.data_models import Game
from user.data_models import LocalUser

def get_count():
    q = Quiz.query().count()
    q_pup = Quiz.query().filter(Quiz.status==1).count()
    g = Game.query().count()
    g_pup = Game.query().filter(Quiz.status==1).count()
    u = LocalUser.query().count()
    return {'q':q, 'q_pup':q_pup, 'g':g, 'g_pup':g_pup,'u':u}

class GetAdminCount(MainHandler):
    """docstring for GetAdminCount"""
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(get_count()))

        
class AdminHome(MainHandler):
    def get(self):
        if self.admin :
            quizes_nv = Quiz.not_verified(n=20)
            games_nv = Game.not_verified(n=20)
            count = get_count()
            self.render('/admin/admin-dash.html',quizes_nv=quizes_nv,games_nv=games_nv,count=count)
            return
        self.redirect('/login')
        

#Add New Admin 
class AddAdmin(MainHandler):
    def get(self):
        if not self.admin :
            self.render('404.html')
        else :
            self.render('/admin/add-admin.html')
    def post(self):
        if not self.admin :
            self.render('404.html')
        else :
            email = self.request.get('email')
            u = LocalUser.by_email(email)
            if not u :
                error = "yes"
                self.render('/admin/add-admin.html',error=error)
            else :
                u.role = '/admin'
                u.put()
                self.render('/admin/add-admin.html', done = 'yes')