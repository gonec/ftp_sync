from ftplib import FTP 
import os
import os.path
import configparser
class Curator:
	#def __init__(self, config_file='sync.ini'):
	def __init__(self, base_dir, cfg_file="sync.ini"):
		print('INIT CURATOR CFG FILE: ', cfg_file)
		self.msg_dir='/inbox'
		config = configparser.ConfigParser()
		#config.read("../config/{0}".format(config_file)
		config_file_path = os.path.join(base_dir, 'config', cfg_file)
		print ("CURATOR config_file: " + config_file_path)
		if not os.path.exists(config_file_path):
			raise IOError( "not found cfg file {}".format(config_file_path) )		
		print('config file path', config_file_path) 
		config.read(config_file_path)	
		print(config.sections())
		if 'FTP' not in config:
			print ('SECTION NOT FOUND')
		else:
			print('SECTION FOUND')

		host     = config['FTP']['host'] 
		login    = config['FTP']['login']
		password = config['FTP']['password']
		#dr = os.path.abspath(os.curdir)	
		tmp =  config['FTP']['tmp_dir']
		self._tmp_dir = os.path.join(base_dir, tmp)	
		print(self._tmp_dir)	
		if os.path.exists( self._tmp_dir ):		
			print(self._tmp_dir)	
			print("ALREADY EXISTS")		
		else:
			os.mkdir( self._tmp_dir )			
					
		print("WORKING DIR: {}".format(self._tmp_dir) )
		self.prefix="inbox"
		print("Reading from cfg host: {0}, {1}, {2}".format(host, login, password) )
		self.ftp = FTP(host)
		self.ftp.login(login, password)
		self.ftp.cwd(self.prefix)
					
	def messages(self):
		ls = self.ftp.nlst()
		return ls
	
	def download(self, msg):
		print('downloading', msg)	
		filename = os.path.join(self._tmp_dir, msg)	
		lf = open(filename, "wb")
		flDownload = True	
		try:	
			self.ftp.retrbinary("RETR " + msg, lf.write, 8*1024)	
		except:
			flDownload = False	
			print("error dowloading")	
		finally:
			lf.close()
		return flDownload	
	def remove(self, msg):
		#self.ftp.cwd(self.msg_dir)
		print('Curator: deleting...', msg)	
		res = self.ftp.delete(msg)
		return res
	
	def is_exists(self, msg):
		msgs = self.messages()
		return msg in msgs;
	
	def upload(self, uploaded_file):
		f=open(uploaded_file, 'r')
		self.ftp.storbinary("STOR %s" % os.path.basename(uploaded_file), f)	
