from ftplib import FTP 
import os
import os.path
import configparser
class FtpMover:
	#def __init__(self, config_file='sync.ini'):
	def __init__(self, cfg_file="sync.ini"):
		print('INIT FTP_MOVER CFG FILE: ')
		config = configparser.ConfigParser()
		#config.read("../config/{0}".format(config_file)
		config_file_path ="./config/{0}".format(cfg_file)
		if not os.path.exists(config_file_path):
			raise IOError( "not found cfg file {}".format(config_file_path) )		
		print('config file path', config_file_path) 
		config.read(config_file_path)	
		print(config.sections())
		if 'FTP' not in config:
			print ('SECTION NOT FOUND')
		else:
			print('SECTION FOUND')
	
		self.host     = config['REMOTE_FTP']['host'] 
		self.login    = config['REMOTE_FTP']['login']
		self.password = config['REMOTE_FTP']['password']
		#dr = os.path.abspath(os.curdir)	
		
		dr = os.path.abspath(os.curdir)	
		print(dr)
		tmp =  config['FTP']['tmp_dir']
		self._tmp_dir = os.path.join(dr, tmp)
		print("Reading from cfg host: {0}, {1}, {2}".format(self.host, self.login, self.password) )
		self.ftp = FTP(self.host)
		self.ftp.set_debuglevel(2)	
		self.ftp.login(self.login, self.password)
		self.ftp.set_pasv(False)
		print("connected")
		#self.ftp.cwd(self.prefix)
	def re_init(self):
		try:	
			self.ftp = FTP(host)
			self.ftp.set_debuglevel(2)	
			self.ftp.login(login, password)
			self.ftp.set_pasv(False)
			return True
		except:
			return False	
	
	def ping(self):
		self.ftp.voidcmd("NOOP")					
	
	def messages(self):
		ls = self.ftp.nlst()
		return ls
	
	def remove(self, msg):
		#self.ftp.cwd(self.msg_dir)
		print('Curator: deleting...', msg)	
		res = self.ftp.delete(msg)
		return res
	
	def is_exists(self, msg):
		msgs = self.messages()
		return msg in msgs;
	def move(self, file_name):
		print("UPLOADING  FILE {0}".format(file_name) );
		self.upload(file_name)	
	def get_size(self, file_name):
		return self.ftp.size(file_name);			
	
	def upload(self, uploaded_file):
		filename = os.path.join(self._tmp_dir, uploaded_file)	
		f = open(filename, 'rb')
		self.ftp.storbinary( "STOR {0}".format(uploaded_file), f )	
		print("uploaded")