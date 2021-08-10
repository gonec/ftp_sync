from curator import Curator
import random 
import os
import shutil 
print('CURATOR TEST')
test_cfg = 'example.ini'
c = Curator(test_cfg)
#msg = random.choice(messages)

def check_messages():
	ok_result={'msg1.txt', 'msg2.txt', 'msg3.txt'}
	messages = c.messages()
	result_set = set(messages)	
	if ok_result==result_set:
		return True
	else:
		return False

def ready():
	tested_file = 'msg1.txt'
	if c.is_exists(tested_file):
		pass									

def restore():
	tested_file = 'msg1.txt'
	if c.is_exists(tested_file):
		print('No point to restore, file existed on server')
		return False 
	else:
		exmpl_file = os.path.join(os.path.realpath('curator_assets'), tested_file)
		c.upload(exmpl_file)
		if c.is_exists( os.path.basename(exmpl_file) ):
			print('File exists on server. Restored.')
			return True
		else:
			return False
							
def check_download():
	tested_file = 'msg1.txt'
	if not os.path.exists(tested_file):
		res = c.download(tested_file)	
		if  os.path.exists(tested_file):
			print('downloaded...', tested_file )
			os.remove(tested_file)		
			print('removing...', tested_file )
			if restore():
				print('RESTORED OK')
			else:
				print('RESTORED FAILE')	
			return True 
		else:
			print('Downloaded failed')
	else:
		print('File already exists')
		return False

def check_is_exists():
	tested_file = 'msg1.txt'
	fl_exists =c.is_exists(tested_file); 		
	if fl_exists:
		return True
	else:
		return False

def check_remove():
	tested_file = 'msg1.txt'
	#saved_path  = os.path.realpath('curator_tmp')	
	#new_path    = os.path.join(saved_path, tested_file)
	#c.download(tested_file);
	#shutil.copy(tested_file, new_path);
	if c.remove(tested_file):
		restore()
		return True
	else:
		return False
#res=check_messages()
#res=check_download()
#res=check_is_exists()
res = check_remove()
#res = check_remove()
#res = restore()
print(res)
#try:
#	c.download(msg):
#	c.delete(msg)
#except:
#	pass
#finally:
#	c.upload(msg)
