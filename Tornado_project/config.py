#coding:utf-8
import os
import uuid
import base64
cookie_secret = base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)


#Application配置参数
settings = {
	"static_path":os.path.join(os.path.dirname(__file__),"static"),
	"template":os.path.join(os.path.dirname(__file__),"template"),
	"cookie_secret":"QxwmLprsRbS2wsx0wuBWdajjZbjS1k6krTotZHuSwt0=",
	"xsrf_cookies":False,
	"debug":True
	}

#mysql配置
# mysql_options=dict(
# 	host = '127.0.0.1',
# 	# port = 3306,
# 	database='ihome',
# 	user = 'root',
# 	password ='mysql'
# )
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="mysql"
)




#redis配置
redis_options = dict(
	host = '127.0.0.1',
	port = 6379
)

passwd_hash_key = 'QxwmLprsRbS2wsx0wuBWdajjZbjS1k6krTotZHuSwt0='
log_file = os.path.join(os.path.dirname(__file__),"logs/log")
log_level = "debug"

image_url_prefix = ""

