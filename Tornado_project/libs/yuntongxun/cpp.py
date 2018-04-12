#coding=utf-8
from CCPRestSDK import REST
import ConfigParser

#主账号
accountSid = '8a216da862764869016283fc36a101d7';
#主账号Token
accountToken = '026e45088c8c46de9ac0dd74dbb088db';
#应用id
appId = '8a216da862764869016283fc370901de';
#请求地址,格式如下
serverIP='app.cloopen.com';
#请求端口
serverPort = '8883';
#REST版本号
softVersion = '2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class _CPP(object):
	def __init__(self):
		self.rest = REST(serverIP,serverPort,softVersion)
		self.rest.setAccount(accountSid,accountToken)
		self.rest.setAppId(appId)
	@classmethod
	def instance(cls):
		if not hasattr(cls,'_instance'):
			cls._instance = cls()
		return cls._instance

	def sendTemplateSMS(self,to,datas,tempID):
		return self.rest.sendTemplateSMS(to,datas,tempID)
cpp = _CPP.instance()

if __name__=='__main__':
	cpp.sendTemplateSMS('18792718056',['12345','2'],1)


# def Singletion(cls):
# 	_instance = {}
# 	def _singletion(*args,**kwargs):
# 		if cls not in _instance:
# 			_instance[cls] = cls(*args,**kwargs)
# 		return _instance[cls]
# 	return _sigleletion


# @Singletion
# class _CPP(object):
# 	def __init__(self):
# 		rest = REST(serverIP,serverPort,softVersion)
# 		rest.setAccount(accountSid,accountToken)
# 		rest.setAppid(appid)
# 	def sendTemplateSMS(self,to,datas,tempID):
# 		return self.rest.sendTemplateSMS(to,datas,tempID)

# cpp = _CPP()

# if __name__ == '__main__':
# 	cpp.sendTemplateSMS('18792718056',['12345','2'],1)