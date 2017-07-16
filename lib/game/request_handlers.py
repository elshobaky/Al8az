"""
Request handlers for game app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
# importing frequently used handlers
from fu import *
_ = t
# Data Models
from data_models import *
from logs import request_handlers as log
# Add New Game
class AddGame(UploadHandler):
    def get(self):
        if not self.admin:
            self.render('404.html')
        else:
            self.response.headers['Content-Type'] = 'text/html;charset=utf-8'
            upload_url = self.create_upload_url('/admin/addgame')
            self.render('/admin/add-game.html', upload_url=upload_url)
    def post (self):
        have_error = False
        self.title = self.request.get('title')
        self.swf = self.request.get('swf')
        self.details = self.request.get('details')
        self.img = self.request.get('img')
        self.status = self.request.get('status')
        if self.status:
            self.status = 1
        if not self.status:
            self.status = 0
        params = dict(title = self.title,
                      details = self.details,
                      swf = self.swf,
                      img = self.img)
        try:
            self.swf = self.get_uploads('swf')[0].key()
        except:
            have_error = True
            params['error_swf'] = "Cann't upload file"
        try:
            self.img = self.get_uploads('img')[0].key()
        except:
            have_error = True
            params['error_img'] = "Cann't upload image"
        if not self.title:
            have_error = True
            params['error_title'] = "You must add a title"
        if not self.admin:
            have_error = True
        if have_error:
            self.response.headers['Content-Type'] = 'text/html;charset=utf-8'
            upload_url = self.create_upload_url('/admin/addgame')
            params['upload_url'] = upload_url
            self.render('/admin/add-game.html', **params)
        else:
            g = Game.register(self.title,
                          self.swf,
                          self.img,
                          self.details)
            g.status = self.status
            g.put()
            self.render('/admin/add-game.html',done='yes',url=g.key.id())
            
            

# Edit Game
class EditGame(UploadHandler):
    def get(self,gid):
        if not self.admin:
            self.render('404.html')
        else:
            game = Game.by_id(int(gid))
            if not game :
                self.render('404.html')
            else :
                self.response.headers['Content-Type'] = 'text/html;charset=utf-8'
                upload_url = self.create_upload_url('/admin/editgame/%s'%gid)
                self.render('/admin/edit-game.html', game=game, upload_url=upload_url)
    def post (self,gid):
        have_error = False
        gid = self.request.get('gid')
        self.title = self.request.get('title')
        self.details = self.request.get('details')
        self.status = self.request.get('status')
        if self.status:
            self.status = 1
        if not self.status:
            self.status = 0
        try:
            self.swf = self.get_uploads('swf')[0].key()
            swf = True
        except:
            swf = False
        try:
            img = True
            self.img = self.get_uploads('img')[0].key()
        except:
            img = False
        params = dict(title = self.title,
                      details = self.details)
        if not gid:
            self.render('404.html')
        else:
            self.game = Game.by_id(int(gid))
            params['game'] = self.game
            if not self.title:
                have_error = True
                params['error_title'] = "You must add a title"
            if not self.admin:
                have_error = True
            if have_error:
                self.response.headers['Content-Type'] = 'text/html;charset=utf-8'
                upload_url = self.create_upload_url('/admin/addgame')
                params['upload_url'] = upload_url
                self.render('/admin/edit-game.html', **params)
            else:
                self.game.title = self.title
                if swf: self.game.swf = self.swf
                if img: self.game.img = self.img
                self.game.details = self.details ; self.game.status = self.status
                self.game.put()
                self.redirect('/admin')


class GamePerma(MainHandler):
    def get(self,gid):
        game = Game.by_id(int(gid))
        if not game:
            self.render('404.html')
        else:
            self.render('game.html',game=game)
            if self.user:
                log.add_log(self.user.key.id(),
                            self.user.nickname,
                            'g',
                            game.key.id(),
                            game.title)


class Games(MainHandler):
    def get(self):
        p = self.request.get('p')
        if not p or int(p) < 1 :
            p = 1
        games , count = Game.get_page(int(p))
        if count%18 == 0:
            count = count/18
        else:
            count = (count/18)+1
        no = len(games)
        self.render('games.html',games=games,count=count,p=int(p),no=no)