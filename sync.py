from libs.curator import Curator 
from libs.dbsync import DbSync
#from libs.analizer import Analizer 
from libs.error import DbError
from libs.ftp_mover import FtpMover
import time
COORD = 1
NOT_COORD = 2
config_file = 'sync.ini'

script_name = os.path.basename(__file__)
pidfile = os.path.join("/tmp", os.path.splitext(script_name)[0]) + ".pid"

def create_pidfile():
    if os.path.exists(pidfile):
        with open(pidfile, "r") as _file:
            last_pid = int(_file.read())

        # Checking if process is still running
        last_process_cmdline = "/proc/%d/cmdline" % last_pid
       	print(last_process_cmdline) 
	if os.path.exists(last_process_cmdline):
            with open(last_process_cmdline, "r") as _file:
                cmdline = _file.read()
            if script_name in cmdline:
                raise Exception("Script already running...")

    with open(pidfile, "w") as _file:
        pid = str(os.getpid())
        _file.write(pid)

def main_loop():
	try:
		curator = Curator( config_file )
		dbsync = DbSync()
		dbsync.connect()
		mover = FtpMover( config_file )	
		#analizer = Analizer()
	except IOError as e:
		print("EXCEPTION: ", e)
		exit(0)

	try:
		while(True):
			files_list = curator.messages()
			for msg_file in files_list:
				fl =  "Msg_file: {}".format(msg_file) 	
				print("Processing: ", fl)
				if dbsync.is_new(msg_file):
					print("New file {}".format(fl) )	
					if ( curator.download(msg_file) ):
						print("DOWNLOADED OK!")	
						#if analizer.has_coords(msg_file):
						#	coord_type = COORD
							#if mover.move_to_storage(msg_file):
							#	currator.remove(msg_file)
						#else:	
						#	coord_type = NOT_COORD 
						#dbsync.save(msg_file, 0, coord_type )			
						
						dbsync.save(msg_file, 0, 1 )			
						try:	
							mover.move(msg_file)
							file_sz = mover.get_size(msg_file)	
							print( "file moved. Size: {0}".format(file_sz) )
						except ftplib.error_temp as err:	
							print("ERROR! Mover error!")
							while ( False == mover.re_init()):
								time.sleep(10)	
						except:
							print("ERROR! Mover error!")
							while ( False == mover.re_init()):
								time.sleep(10)	

				
					else:
						print("NOT DOWNLOADED")
						next
				else:
					print( "ALREADY PROCESSED: {}".format(fl) );
			try:	
				mover.ping()
			except:
				print("reconnecting")
				mover = FtpMover(config_file)
			time.sleep(10)
	except DbError as e:
		print("DB ERROR")	

if __name__ == "__main__":
	try: 
		create_pidfile()
		main_loop()
	except BaseException as e:
		print(e)


