from dbsync import DbSync 
dbsync = DbSync()
dbsync.connect()
if dbsync.is_new('first'):
	print('WORKS')
dbsync.save('second', 2,2)
