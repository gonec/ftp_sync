class DbError(Exception):
	def __init__(self, text):
		self.txt = text		
