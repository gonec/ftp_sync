from dbsync import DbSync
from dbsync import Message 
dbsync = DbSync()
dbsync.connect()

def test_save_message():
	message=Message('test.msg',1,1)	
	if ( dbsync.save_message(message) ):
		print('SAVED MESsAGE ' + str( dbsync.last_id() ) )
		last_id = dbsync.last_id();
		print('CHECKING SAVED')
		if ( dbsync.is_saved(message) ):
			print( 'SAVED OK!' )
		else:
			print( 'INCORRECT' )	
	else:
		print('NOT SAVED')


def test_message_by_name():
	try:	
		message = dbsync.message_by_name('test.msg')			
		message.show()
	except Exception as e:
		print(str(e))	


test_message_by_name()
