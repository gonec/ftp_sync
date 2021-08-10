import os
import signal

import logging


if __name__ == "__main__":
	
	logging.basicConfig(
		filename="/tmp/sync.log",
		level=logging.INFO,
		format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
		#filemode = 'w', )
		filemode = 'a', )
	logger = logging.getLogger(__name__)
	
	pidfile = "/tmp/sync.pid"
	with open(pidfile, "r") as fh:
		last_pid = int( fh.read() )
		
	try:
		os.kill( last_pid, signal.SIGKILL )
		logger.warning( "Process killed: {0:d}...".format(last_pid) )
	except Exception:
		logger.info("NOT RUN...")
