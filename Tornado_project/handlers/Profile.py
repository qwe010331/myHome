#coding:utf-8
import logging
import config
from utils.response_code import RET
from utils.commons import require_logined
from .BaseHandler import BaseHandler
from utils.image_storage import storage

class AvatarHandler(BaseHandler):
	""""""
	@require_logined
	def post(self):
		user_id = self.session.data['user_id']
		# try:
		# 	image_data = self.request.files["avater"][0]["body"]
		# 	if not image_data:
		# 		return self.write(dict(errno =RET.PARAMERR, errmsg ="未传图片" )
		# except Exception as e:
		# 	logging.error(e)
		# 	return self.write("")
		try:
			key = storage(image_data)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno =RET.PARAMERR, errmsg="上传失败"))
		try:
			self.db.execute("update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s",avatar = image_data,user_id =user_id )
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR, errmsg="保存错误"))
		else:
			return self.write(dict(errno = RET.OK, errmsg="保存成功", data="%s%s" %(config.image_url_prefix,image_data) ))


class ProfileHandler(BaseHandler):
	@require_logined
	def get(self):
		user_id = self.session.data['user_id']
		try:
			# ret = self.db.get("select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%(user_id)s", user_id)
			ret = self.db.get("select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s", user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR,errmsg = 'get data error'))
		if ret['up_avatar']:
			image_url = config.image_url_prefix + ret['up_avatar']
		else:
			image_url = None
		return self.write(dict(errno = RET.OK,errmsg = 'OK',data = dict(user_id=user_id,name = ret['up_name'],mobile = ret['up_mobile'],avatar = image_url)))


class NameHandler(BaseHandler):
	@require_logined
	def post(self):
		user_id = self.session.data['user_id']
		user_name = self.json_args.get('name')
		if not user_name:
			return self.write(dict(errno = RET.PARAMERR,errmsg = '用户名出错'))
		try:
			ret = self.db.execute("update ih_user_profile set up_name=%(name)s where up_user_id=%(user_id)s", name = user_name, user_id = user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR, errmsg = "用户名已经存在"))

		self.session.data['name'] = user_name
		try:
			self.session.save()
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR,errmsg = 'session保存失败'))
		else:
			return self.write(dict(errno = RET.OK,errmsg = '保存成功'))


class AuthHandler(BaseHandler):
	@require_logined
	def get(self):
		user_id = self.session.data['user_id']
		try:
			ret = self.db.get("select up_real_name,up_id_card from ih_user_profile where up_user_id=%(user_id)s", user_id = user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno = RET.DBERR,errmsg = '数据不存在'))
		if not ret:
			return self.write(dict(errno = RET.NODATA,errmsg = '数据不存在'))
		else:
			self.write(dict(errno = RET.OK,errmsg ='OK',data = dict(id_card = ret['up_id_card'],real_name = ret['up_real_name'])))
	@require_logined
	def post(self):
		user_id = self.session.data['user_id']
		real_name = self.json_args.get('real_name')
		id_card = self.json_args.get('id_card')
		if user_id and real_name and id_card:
			if len(id_card) != 18:
				return self.write(dict(errno = RET.PARAMERR,errmsg = '请填写正确身份证号码')) 
			try:
				self.db.execute("update ih_user_profile set up_real_name=%(real_name)s,up_id_card=%(id_card)s where up_user_id=%(user_id)s", real_name = real_name, id_card = id_card, user_id = user_id)
			except Exception as e:
				logging.error(e)
				return self.write(dict(errno = RET.DBERR,errmsg = '保存失败'))
			else:
				return self.write(dict(errno = RET.OK,errmsg = '保存成功'))
		else:
			return self.write(dict(errno = RET.PARAMERR,errmsg = '请填写完整数据'))






