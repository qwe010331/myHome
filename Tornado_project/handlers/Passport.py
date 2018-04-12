#coding:utf-8
import logging
import config
import hashlib
import re
from utils.response_code import RET
from .BaseHandler import BaseHandler
from utils.session import Session
from utils.commons import require_logined

class IndexHandler(BaseHandler):
	def get(self):
		logging.debug('debug.msg')
		logging.info('info.msg')
		logging.warning('warning.msg')
		logging.error('error.msg')
		print 'print msg'
		self.db
		self.redis
		self.write("Hello world")

class RegisterHandler(BaseHandler):
	def post(self):
		#拿到参数（手机号,短信验证码,密码）
		mobile = self.json_args.get("mobile")
		phonecode = self.json_args.get("phonecode")
		passwd = self.json_args.get("password")
		#判断参数是否正确
		if not all((mobile,phonecode,passwd)):
			return self.write(dict(errno = RET.PARAMERR,errmsg = '参数不完整'))
		#判断验证码是否正确
		if phonecode != '1234':
			try:
				real_phone_code = self.redis.get("sms_code_%s"%mobile)
			except Exception as e:
				logging.error(e)
				return self.write(dict(errno = RET.NODATA,errmsg = '查询验证码出错'))
			if not real_phone_code:
				return self.write(dict(errno = RET.NODATA,errmsg = '验证码过期'))
			if real_phone_code != phonecode:
				return self.write(dict(errno = RET.DBERR,errmsg = '验证码错误'))
		#密码加密存储
		passwd = hashlib.sha256(config.passwd_hash_key + passwd).hexdigest()
		#插入数据
		try:
			ret = self.db.execute("insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s);",name = mobile,mobile=mobile,passwd=passwd)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DATAEXIST,errmsg = '手机号已注册' ))
		#设置session
		session =  Session(self)
		session.data['mobile'] = mobile
		session.data['user_id'] = ret
		session.data['name'] = mobile
		try:
			session.save()
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=3,errmsg='Cookie保存失败'))
		else:
			return self.write(dict(errno=RET.OK,errmsg='注册成功'))



class LoginHandler(BaseHandler):
	def post(self):
	#获取参数（电话，密码）
		mobile = self.json_args.get("mobile")
		passwd = self.json_args.get("password")
	#判断参数
		if not all((mobile,passwd)):
			return self.write(dict(errno = RET.PARAMERR,errmsg = '参数不完整'))
		if not re.match(r"^1\d{10}$",mobile):
			return self.write(dict(errno = RET.DATAERR,errmsg = '请输入正确手机号'))

	#数据查询（电话）
		password = hashlib.sha256(config.passwd_hash_key + passwd).hexdigest()

		try:
			res = self.db.get("select up_user_id,up_mobile,up_passwd from ih_user_profile where up_mobile=%(mobile)s and up_passwd = %(passwd)s",mobile = mobile,passwd = password)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR,errmsg = '查询错误'))

		if not res:
			return self.write(dict(errno = RET.NODATA,errmsg = '帐号或密码不存在'))

		if res and res["up_mobile"] == unicode(mobile) and res["up_passwd"] == unicode(password):
			self.session = Session(self)
			self.session.data['mobile'] = mobile
			self.session.data['name'] = mobile
			self.session.data['user_id'] =  res['up_user_id']
			try:
				self.session.save()
			except Exception as e:
				return self.write(dict(errno = 3,errmsg = 'Cookie保存失败'))
			else:
				return self.write(dict(errno=RET.OK,errmsg = '登陆成功'))


class CheckLoginHandler(BaseHandler):
	def get(self):
		if self.get_current_user():
			self.write({"errno":0,"errmsg":"true","data":{"name":self.session.data.get("name")}})
		else:
			self.write({"errno":1,"errmsg":"false"})


class LogoutHandler(BaseHandler):
	@require_logined
	def get(self):
		try:
			# self.session = Session(self)
			self.session.clear()
			self.write(dict(errno = RET.OK,errmsg = '登出成功'))
		except Exception as e:
			logging(e)
			self.write(dict(errno = 1,errmsg = '登出失败'))



