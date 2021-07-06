import mysql.connector
from libs.error import DbError
class Message():
	def __init__(self, file_name, status, msg_type):
		print('CREATING MESSAGE')
		self.file_name = file_name
		self.status = status
		self.msg_type = msg_type	
		self.msg_id = -1		
		print('FILE NAME', file_name)	
		print('STATUS   ', status)	
		print('TYPE     ', msg_type)	
		print('created')
	
	def __eq__(self, other):
		return ( (self.file_name == other.name) and (self.msg_type == other.msg_type) and (self.status == other.status) )

	def show(self):
		print("Message  FILE_NAME: {0} STATUS: {1} MSG_TYPE: {2} MSG_ID: {3}".format(self.file_name, self.status, self.msg_type, self.msg_id))

class DbSync:
	def __init__(self, ignore = True):
		self.ignore = ignore
	
	def connect(self):
		try:
			self._connection = mysql.connector.connect(host='192.168.20.199',
							 database='downloader',
							 user='alarm',
							 password='alarmuser')

			if self._connection.is_connected():
				db_Info = self._connection.get_server_info()
				print("Connected to MySQL Server version ", db_Info)
				self.cursor = self._connection.cursor()
				self.cursor.execute("select database();")
				record = self.cursor.fetchone()
				print("Your connected to database: ", record)	
			else:
				raise IOError("Connection problem 1")	
		except:
			raise IOError("Connection problem 2")	
	
	def is_new(self,msg):
		sql_select_query = "SELECT * FROM files WHERE file_name=\'{0}\'".format(msg) 
		#print("QUERY: {}".format(sql_select_query) )
		cursor = self._connection.cursor()
		cursor.execute(sql_select_query)
		records=cursor.fetchall()
		#print("NUMBER OF RECORDS", cursor.rowcount)
		if cursor.rowcount == 0:
			return True		
		if cursor.rowcount == 1:
			return False	
		else:
			raise DbError("DB ERROR!")

	def save_message(self, message):
		 return self.save(message.file_name, message.status, message.msg_type)			
	
	def is_saved(self, message):
		if self.is_new( message.file_name):
			return False
		else:
			return True						

	def save(self, msg, status, msg_type):
		try:
			sql_insert_query = "INSERT INTO files (file_name, status, msg_type) VALUES (\'{0}\', {1}, {2})".format(msg, status, msg_type)
			cursor = self._connection.cursor()
			cursor.execute(sql_insert_query)
			self._connection.commit()
			self.insert_id = cursor.lastrowid	
			print ("LAST ROW ID: ", self.insert_id)
			row_count = cursor.rowcount
			if row_count == 1:
				return True
			else:
				return False

		except:
			return False	
	def update_status (self, id,  status):
		query = "UPDATE files SET status={0} WHERE id={1}".format(status, id)	
		cursor = self._connection.cursor()
		cursor.execute(query)
		self._connection.commit()

	
	def last_id(self):
		return self.insert_id

	def message_by_name(self, file_name):
		sql_select_query = "SELECT * FROM files WHERE file_name=\'{0}\'".format(file_name) 
		cursor = self._connection.cursor()
		cursor.execute(sql_select_query)
		records=cursor.fetchall()
		#print("NUMBER OF RECORDS", cursor.rowcount)
		#print(records)
		row = records[0]
		#print('row', row)
			
		if cursor.rowcount == 1:
			status   = row[2]
			msg_type = row[3]	
			return Message(file_name, status, msg_type)	
		elif ( cursor.rowcount > 1) and self.ignore:
			status   = row[2]
			msg_type = row[3]	
			return Message(file_name, status, msg_type)	
		else:
			raise Exception('integrity error')	
	
	def message_by_id(self, id):
		pass
						 
