# coding:utf-8
from qiniu import Auth
from qiniu import Auth,put_file,etag,urlsafe_base64_encode
import qiniu.config

def storage(image_data):
	if not image_data:
		return None
	accrss_key = 'gwpnQF2hx4S2NhEUsA9DSHUteI4cb3aqpAApTPzT'
	secret_key = '1g3qEeTxgsAU4ZMdTdlTK9gIcW1eC631BXnyaq1A'
	#构建鉴权对象
	q = Auth(access_key, secret_key)
	#要上传的空间
	bucket_name = 'Ihome'
	#上传到七牛后保存的文件名
	# key = 'my-python-logo.png';
	#生成上传 Token，可以指定过期时间等
	token = q.upload_token(bucket_name, None, 3600)
	#要上传文件的本地路径
	localfile = './sync/bbb.jpg'
	ret, info = put_file(token, None, localfile)
	print(info)
	# assert ret['key'] == key
	# assert ret['hash'] == etag(localfile)
	return ret['key']


if __name__=="__main__":
	file_name = raw_input("请输入文件名：")
	file = open(file_name,'rb')
	file_data = file.read()
	key = storage(file_data)
	print key
	file.close()










