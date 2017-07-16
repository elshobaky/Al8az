from fu import *
#from quiz.data_models import Quiz
from user.data_models import LocalUser, User
from quiz.data_models import Quiz
from game.data_models import Game


# home page handler
class MainPage(MainHandler):
    def get(self):
        full_quiz = Quiz.random(count=2,filters=[Quiz.status==1])
        quizes = Quiz.rss(n=8)
        games = Game.random(count=10,filters=[Game.status==1])
        no = len(games)
        self.render('home.html', full_quiz=full_quiz,quizes=quizes,games=games,home=True)
        #self.render('home.html', home=True)

class GetStars(MainHandler):
    def get(self):
        stars = LocalUser.get_stars(ajax=True)
        self.response.headers['Content-Type'] = 'application/json'
        self.write(stars)


class RSS(MainHandler):
    def get(self):
        s = self.request.get('s')
        if not s :
            s = '0'
        n = self.request.get('n')
        if not n:
            n = '50'
        if int(n) > 500 :
            n = '500'
        quiz = Quiz.rss(s=int(s), n=int(n))
        self.response.headers['Content-Type'] = 'text/xml'
        self.render("rss.xml", quiz=quiz, mimetype='application/xml')


class GameRSS(MainHandler):
    def get(self):
        s = self.request.get('s')
        if not s :
            s = '0'
        n = self.request.get('n')
        if not n:
            n = '50'
        if int(n) > 500 :
            n = '500'
        game = Game.rss(s=int(s), n=int(n))
        self.response.headers['Content-Type'] = 'text/xml'
        self.render("game-rss.xml", game=game, mimetype='application/xml')


class UP(MainHandler):
    'script update handler'
    def get(self):
        """
        old_users = User.query().fetch()
        for user in old_users:
            if user.role == 'user':
                user.role = 'u'
            u = LocalUser.signup(firstname=user.firstname,
                                   lastname=user.lastname,
                                   nickname='%s %s' %(user.firstname, user.lastname),
                                   pw_hash=user.pw_hash,
                                   email=user.email,
                                   role=user.role,
                                   group = 'default')
            u.about = user.about
            u.country = user.country
            u.score = user.score
            u.todayscore = user.todayscore
            u.q_solved = user.q_solved
            u.q_try = user.q_try
            u.g_play = user.g_play
            u.rate = user.rate
            #u.level = user.level
            u.contact = user.contact
            u.put()
        """
        self.write('done')
            
        
class Search(MainHandler):
    def get(self):
        self.render('search.html')