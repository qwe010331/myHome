#coding:utf-8
import os
from handlers import Passport,VerifyCode,Profile
# from handlers import BaseHandler
from handlers.BaseHandler import StaticFileHandler


handlers = [
	# (r"/",Passport.IndexHandler),
	(r"/api/register",Passport.RegisterHandler),
	(r"/api/imageccode",VerifyCode.ImageCodeHandler),
	(r"/api/smscode",VerifyCode.SMSCodeHandler),
	(r"/api/login",Passport.LoginHandler),
	(r"/api/check_login",Passport.CheckLoginHandler),
	(r"/api/profile",Profile.ProfileHandler),
	(r"/api/profile/name",Profile.NameHandler),
	(r"/api/profile/auth",Profile.AuthHandler),
	(r"/api/logout",Passport.LogoutHandler),
	(r"/(.*)",StaticFileHandler,dict(path = os.path.join(os.path.dirname(__file__),"html"),default_filename ='index.html'))
]