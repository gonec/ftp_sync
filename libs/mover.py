import os
import configparser
class Mover():
	def __init__(self, config_file):
		config = configparser.ConfigParser()
		#config.read("../config/{0}".format(config_file)
		config_file_path = "./config/{0}".format(config_file)
		if not os.path.exists(config_file_path):
			raise IOError( "not found cfg file {}".format(config_file_path) )		
		config.read(config_file_path)	
		if 'STORAGE' not in config:
			raise IOError("SECTION [STORAGE] NOT FOUND")	
		self._processing_dir = config['STORAGE']['processing'] 
		if not os.path.exists(self._processing_dir):
			print("Mover: making dir")	
			os.mkdir(self._processing_dir)
			#raise IOError("path not exists")	
					
	def move_to_storage(self, fl):
		to = self._processing_dir
		print("moving file {} to {}".format(fl, to) )
		try:
			shutil.move(fl, os.path.join(to, os.path.basename(fl)))
		except:
			raise IOError("can not move file")
	def remove(self, fl):
		os.remove(fl)						
	
	def clear(self, msg_file):
		nop
