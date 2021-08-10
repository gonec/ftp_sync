import ftplib
import os
import os.path
import configparser

import logging
 
logging.basicConfig(
	filename="/tmp/sync.log",
	level=logging.INFO,
	format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
logger = logging.getLogger(__name__)

class FtpMover:
	#def __init__(self, config_file='sync.ini'):
	def __init__(self, base_dir,  cfg_file="sync.ini"):
		"""Constructor"""
		print('INIT FTP_MOVER CFG FILE: ')
		config = configparser.ConfigParser()
		#config.read("../config/{0}".format(config_file)
		config_file_path = os.path.join(base_dir, "config", cfg_file)
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
		self._tmp_dir = os.path.join(base_dir, tmp)
		print("Reading from cfg host: {0}, {1}, {2}".format(self.host, self.login, self.password) )
	
		self.ftp = self.get_ftp_connection()
		print( "FTP Connection ok..." )
		logger.info( "FTP Connection ok..." )
		#self.ftp.cwd(self.prefix)
		
	def get_ftp_connection(self):
		""" Возвращаем ФТП соединение """
		ftp = ftplib.FTP(self.host)
		ftp.set_debuglevel(2)
		ftp.set_pasv(False)
		ftp.login(self.login, self.password)
		return ftp;

	def re_init(self):
		try:	
			self.ftp = ftplib.FTP( self.host )
			self.ftp.set_debuglevel(2)	
			self.ftp.login( self.login, self.password )
			self.ftp.set_pasv(False)
			logger.info( "FTP Connection ok..." )
			return True
		except:
			logger.error( "Connection false..." )
			return False	
	
	def ping(self):
		self.ftp.voidcmd("NOOP")					
	
	def messages(self):
		ls = self.ftp.nlst()
		return ls
	
	def remove(self, msg):
		#self.ftp.cwd(self.msg_dir)
		print('FtpMover: deleting...', msg)
		logger.info('FtpMover: deleting...' + msg)
		res = self.ftp.delete(msg)
		return res
	
	def is_exists(self, msg):
		msgs = self.messages()
		return msg in msgs;
	
	def move(self, file_name):
		print("UPLOADING  FILE {0}".format(file_name) )
		logger.info( "UPLOADING...  FILE {0}".format(file_name) )
		self.upload(file_name)
		logger.info( "Uploading done. {0}".format(file_name) )
		
	def get_size(self, file_name):
		return self.ftp.size(file_name);			
	
	def upload(self, uploaded_file):
		# ftp = self.get_ftp_connection()
		filename = os.path.join(self._tmp_dir, uploaded_file)	
		f = open(filename, 'rb')
		ftpResponseMessage = self.ftp.storbinary( "STOR {0}".format(uploaded_file), f )
		print( ftpResponseMessage )
		logger.info( ftpResponseMessage )
		f.close()
