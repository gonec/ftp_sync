#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from  xml.dom.minidom import parse, parseString

class Analizer():
	def get_data(self, body, pos, length):
		dt = body[2*pos : 2*pos + 2*length]	
		return(dt)	


	def hat_size_ok(self, body):
		hat_size = get_hat_size(body)	
		return True

	def zero_ok(self, body):
		zer = get_zero(body)	
		if zer==0:
			return True
		else:
			return False

	def coord_message(self, data):
		if  not zero_ok(data):
			print("ZERO ERROR")
			return False	
		elif not hat_size_ok(data):
			print("HAT ERROR")
			return False		
		elif not version_ok(data):
			print("VERSION ERROR")
			return False 
		else:
			return True	

	def version_ok(self, data):
		version = get_version(data)
		return True

	def get_version(self, body):
		pos = 10 
		size = 1 
		data = get_data(body, pos, size)
		return data

	def get_at_num(self, body):
		pos = 12 
		size = 4 
		data = get_data(body, pos, size)
		return data

	def get_hat_size(self, body):
		pos = 11
		size = 1 
		data = get_data(body, pos, size )
		return data

	def get_zero(self, body):
		pos = 9 
		size = 1 
		data = get_data(body, pos, size )
		return data

	def has_coords(self, fl):
		datasource = open(fl)
		try:	
			dom = parse(datasource)
			body =dom.getElementsByTagName('body')[0]
			body_str = body.firstChild.nodeValue
			#print(body_str)
			#hx=body_str[0:2]
			#n = int(hx,16)
			#print(n)
			#list_of_bytes = map(ord, body_str.encode('utf8'))
			#print(type(body_str))
			#print(list_of_bytes)
			at	= get_at_num(body_str) 
			hat_sz  = get_hat_size(body_str)
			zr 	= get_zero(body_str)
			version = get_version(body_str)
			print("=========================")
			#print("AT: %s " % at)
			#print("HAT: %s " % hat_sz)
			#print("ZERO: %s " % zr)
			#print("VERSION: %s " % version)
			datasource.close()
			if coord_message(body_str):
				#print("COORD MESSAGE!")
				return True
			else:
				#print("NOT CORD")
				return False 

		except:
			datasource.close()
			return False
#file_name="20190622145150_761_ЦУСК_DOWN_D2_3468220_20190622145133.msg"

print(os.getcwd())	
	
ls = os.listdir(".");
for el in ls:
	ext = os.path.splitext(el)[1]
	if ext==".msg":
		print("testing file...: %s" % el)
		if ( test_file(el) ):
			print("FILE: %s is COORDFILE" % el)	
		else:
			print("FILE: %s not COORDFILE" % el)


	else:
		print("incorrect extension %s" % ext)

