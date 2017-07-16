"""
Request handlers for user app a part of OpenAl8az project.
By : Mahmoud Elshobaky (mahmoud.elshobaky@gmail.com).
"""
# importing frequently used handlers
from fu import *
# google users api
from google.appengine.api import users
# Data Models
from data_models import *
# File data model for storing upladed file info
from files.data_models import File
# form inputs validators
from MeX.validators import *

class SignUp(MainHandler):
	"""user signup handler"""
	def get(self):
		ref = self.request.get('ref')
		login_url = users.create_login_url(ref or self.uri_for('home-page'))
		if self.request.get('ajax') == 't':
			self.render('signup-form.html', login_url=login_url)
			return
		self.render('signup.html', login_url=login_url)
	def post(self):
		have_error = False
		self.firstname = self.request.get('firstname')
		self.lastname = self.request.get('lastname')
		self.email = self.request.get('email')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.ajax = self.request.get('ajax')

		params = dict(firstname = self.firstname,
			          lastname = self.lastname,
			          email = self.email)

		if not valid_name(self.firstname) or not valid_name(self.lastname):
			have_error = True
			params['error_name'] = t('name is not valid')

		if not valid_email(self.email):
			have_error = True
			params['error_email'] = t('email is not valid')

		if not valid_password(self.password):
			have_error = True
			params['error_password'] = t('password is not valid')
		elif self.password != self.verify:
			have_error = True
			params['error_verify'] = t('password do not match')

		if have_error:
			if self.ajax == 't':
				params['signup'] = False
				self.write_json(params)
				return
			self.render('signup.html', **params)
			return

		if LocalUser.by_email(self.email):
			error_email = 'email already exists'
			if self.ajax == 't':
				self.write_json({'signup':False, 'error_email':error_email})
				return
			self.render('signup.html', error_email=error_email)
			return
		self.nickname = '%s %s' %(self.firstname, self.lastname)
		self.pw_hash = make_pw_hash(self.email, self.password)
		u = LocalUser.signup(self.firstname,
			                 self.lastname,
			                 self.nickname,
			                 self.pw_hash,
			                 self.email,
			                 role='user')
		u.put()
		self.login(u)
		self.add_flash(t('thanks! for signing up please, go to ') +\
                         '<a href="/user/profile">%s</a>'% t('your profile') +\
                         t(' to update your info'),'success')
		if self.ajax == 't':
			self.write_json({'signup':True})
			return
		self.redirect_to('home-page')


class LogIn(MainHandler):
	"""user login handler"""
	def get(self):
		if not self.user:
			ref = self.request.get('ref')
			login_url = users.create_login_url(ref or self.uri_for('home-page'))
			if self.request.get('ajax') == 't':
				self.render('login-form.html',login_url=login_url)
				return
			self.render('login.html',login_url=login_url)
			return
		self.add_flash('your are already signed in', 'danger')
		self.redirect_to('home-page')
	def post(self):
		email = self.request.get('email')
		password = self.request.get('password')
		ajax = self.request.get('ajax')
		ref = self.request.get('ref')
		u = LocalUser.login(email, password)
		if u:
			self.login(u)
		if u and ajax == 't':
			self.write_json({'login':True})
		elif ajax == 't':
			self.write_json({'login':False})
		elif u:
			self.redirect(ref or self.uri_for('home-page'))
		else:
			self.render('login.html', error=t('invalid email or password'), email=email)

class LogOut(MainHandler):
	"""user logout handler"""
	def get(self):
		self.logout()
		if self.google_user:
			logout_url = users.create_logout_url(self.uri_for('home-page'))
			self.redirect(logout_url)
			return
		self.redirect_to('home-page')

class Profile(MainHandler):
	"""user profile handler"""
	def get(self, user_id):
		u = LocalUser.by_id(int(user_id))
		if not u:
			self.render('404.html')
			return
		if self.user and self.user.key.id() == u.key.id():
			self.redirect_to('my-profile')
			return
		self.render('puplic-profile/profile.html',page=True, p_user = u, uid = u.key.id())
		return

class MyProfile(UploadHandler):
	"""view and edit user own profile"""
	def get(self):
		if not self.user:
			self.redirect_to('user-login',ref=self.uri_for('my-profile'))
			return
		upload_url = self.create_upload_url('/user/profile/changeavatar')
		self.render('profile/profile.html',page=True,upload_url=upload_url)
	def post(self):
		if not self.user:
			self.redirect_to('user-login', ref=self.uri_for('my-profile'))
			return
		have_error = False
		# getting data from POST params
		self.ajax = self.request.get('ajax')
		self.firstname = self.request.get('firstname')
		self.lastname = self.request.get('lastname')
		self.email = self.request.get('email')
		self.password = self.request.get('password')
		self.country = self.request.get('country')
		self.about = self.request.get('about')
		upload_url = self.create_upload_url('/user/profile/changeavatar')
		# preparing response params in case there is an error
		params = dict(firstname = self.firstname,
			          lastname = self.lastname,
			          email = self.email,
			          about = self.about,
			          country = self.country,
			          upload_url = upload_url,
			          page = True)
		# validating user inputs
		if not valid_name(self.firstname) or not valid_name(self.lastname):
			have_error = True
			params['error_name'] = t('name is not valid')
		if not valid_email(self.email):
			have_error = True
			params['error_email'] = t('email is not valid')
		elif self.email != self.local_user.email:
			if LocalUser.by_email(self.email):
				have_error = True
				params['error_email'] = t('email is used in an other account')
		if self.password and not valid_password(self.password):
			have_error = True
			params['error_password'] = t('password is not valid')
		if have_error:
			if self.ajax == 't':
				params['edit_profile'] = False
				self.write_json(params)
			else:
				self.render('profile/profile.html',**params)
			return
		u = LocalUser.by_id(self.local_user.key.id())
		u.firstname = self.firstname
		u.lastname = self.lastname
		u.nickname = '%s %s' %(self.firstname, self.lastname)
		u.email = self.email
		u.pw_hash = make_pw_hash(self.email, self.password)
		u.about = self.about
		u.country = self.country
		u.put()
		if self.ajax == 't':
			params['edit_profile'] = True
			self.write_json(params)
			return
		self.redirect_to('my-profile')


class ChangeAvatar(UploadHandler):
	""" change user avatar . only post request"""
	def post(self):
		if not self.user:
			self.redirect_to('user-login', ref=self.uri_for('my-profile'))
			return
		try:
			uploaded_file = self.get_uploads('avatar')[0]
			file_key = uploaded_file.key()
			file_info = self.get_info(file_key)
			file_name = file_info.filename
			file_size = file_info.size
			content_type = file_info.content_type
			f = File.add_file(self.local_user.key.id(),
				     self.local_user.nickname,
				     file_key,
				     file_name,
				     file_size,
				     content_type)
			f.put()
			if f.content_type.startswith('image'):
				self.avatar = f.key.id()
				if self.local_user.avatar:
					File.delete_file(self.local_user.avatar)
			else:
				f.delete_me()
				self.avatar = self.local_user.avatar
		except:
			self.avatar = self.local_user.avatar

		u = LocalUser.by_id(self.local_user.key.id())
		u.avatar = self.avatar
		u.put()
		self.add_flash(t('Your avatar has been updated'),'success')
		self.redirect_to('my-profile')

class ChangeContact(MainHandler):
	"""change user social media urls . post request only"""
	def post(self):
		have_error = False
		if not self.user:
			self.redirect_to('user-login', ref=self.uri_for('my-profile'))
			return
		f = self.request.get('f')
		tw = self.request.get('t')
		g = self.request.get('g')
		i = self.request.get('i')
		ajax = self.request.get('ajax')
		params = dict(f=f, t=tw, g=g, i=i, page=True)
		if f and not valid_url(f):
			have_error = True
			params['error_f'] = t('url not vaild')
		if tw and not valid_url(tw):
			have_error = True
			params['error_t'] = t('URL not vaild')
		if g and not valid_url(g):
			have_error = True
			params['error_g'] = t('URL not vaild')
		if i and not valid_url(i):
			have_error = True
			params['error_i'] = t('URL not vaild')
		if have_error:
			if ajax == 't':
				params['change_contact'] = False
				self.write_json(params)
				return
			self.render('profile/profile.html',**params)
			return
		LocalUser.update_contact(self.local_user.key.id(),
			                f, tw, g, i)
		if self.request.get('ajax') == 't':
			self.response.headers['Content-Type'] ='application/json'
			self.write(json.dumps({'change_contact':True}))
			return
		self.redirect_to('my-profile')