#coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import config
import torndb
import redis
from  tornado.options import define,options 
from tornado.web import RequestHandler
from url import handlers 


define('port',type=int,default=8000,help='run server on th given port')

class Application(tornado.web.Application):
	""""""
	def __init__(self,*args,**kwargs):
		super(Application,self).__init__(*args,**kwargs)
		# self.db = torndb.Connection(
		#    	host = config.mysql_options['host'],
		# 	database= config.mysql_options['database'],
		# 	user = config.mysql_options['user'],
		# 	password = config.mysql_options['password']
		# )
		# self.db = torndb.Connection(**config.mysql_options)
		self.db = torndb.Connection(**config.mysql_options)
		# self.db = torndb.Connection("127.0.0.1","ihome",'root','mysql')
		# sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s, %(mobile)s, %(passwd)s);"
  # 		mobile='18258171245'
  # 		name = '18258171245'
  # 		passwd = '123456'
  # 		self.db.execute(sql,name = mobile,mobile = mobile,passwd = passwd)
		# self.redis = redis.StrictRedis(
		#     host = config.redis_options['host'],
		#     port = config.redis_options['port']
		#                                )
		self.redis = redis.StrictRedis(**config.redis_options)
def main():
	options.logging = config.log_level
	options.log_file_prefix = config.log_file
	tornado.options.parse_command_line()
	settings = {

	}
	app = Application(
			handlers,**config.settings
	                              )
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	# http_server.bind(8000)
	# http_server.start(0)
	tornado.ioloop.IOLoop.current().start()




if __name__=='__main__':
	main()