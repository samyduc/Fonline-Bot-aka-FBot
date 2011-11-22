import zlib
import gzip
import binascii
import socket
import struct
import os, sys
import smtplib
from email.MIMEText import MIMEText

class Futils:
	#####################################################################
	#Encode login and password											#
	#####################################################################
	def string_to_encode(u_string, taille):
		e_string = u_string.encode("hex")
		if(len(e_string) != taille):
			e_string = e_string + "0"*(taille - len(e_string))
		return e_string
	string_to_encode = staticmethod(string_to_encode)
	
	def int_to_encode(u_int, taille):
		e_int = hex(u_int)[2:]
		# hack for small number because big endian
		if(u_int < 16):
			e_int = '0' + e_int
		if(len(e_int) != taille):
			e_int = e_int + "0"*(taille - len(e_int))
		return e_int
	int_to_encode = staticmethod(int_to_encode)
	
	def integer_to_hex(u_integer):
		data = socket.htons(u_integer)
		hex_data = hex(data)[2:]
		return hex_data
	integer_to_hex = staticmethod(integer_to_hex)
	
	def integer_to_encode(u_integer, taille):
		hex_data = Futils.integer_to_hex(u_integer)
		if(len(hex_data) != taille):
			e_data = hex_data + "0"*(taille - len(hex_data))
		return e_data
	integer_to_encode = staticmethod(integer_to_encode)
	#####################################################################
	#Decompresse, Compress data from the server.						#
	#####################################################################
	def wireshark_to_compressed(w_data):
		c_data = w_data.replace(':', '')
		try:
			c_data = binascii.unhexlify(c_data)
		except:
			print("Futils::wireshark_to_compressed error " + c_data)
		return c_data
	wireshark_to_compressed = staticmethod(wireshark_to_compressed)
		
	def decompress(c_data):
		try:
			o_data = zlib.decompressobj()
			u_data = o_data.decompress(c_data)
		except zlib.error as e:
			print("Futils::decompress " + str(e))
			u_data = str(c_data)
		return u_data
	decompress = staticmethod(decompress)
	
	def hex_to_wireshark(hex_data):
		if(len(hex_data) > 2):
			w_data = hex_data[:2]
			for i in range(len(hex_data)/2 - 1):
				i = i + 1
				w_data  = w_data + ":" + hex_data[i*2:i*2+2]
			if(len(hex_data) % 2 != 0):
				w_data = w_data + ":" + hex_data[len(hex_data)-1:]
		else:
			w_data = hex_data
		return w_data
	hex_to_wireshark = staticmethod(hex_to_wireshark)	
	
	def wireshark_to_uncompressed(w_data):
		c_data = Futils.wireshark_to_compressed(w_data)
		u_data = Futils.decompress(c_data)
		return u_data
	wireshark_to_uncompressed = staticmethod(wireshark_to_uncompressed)	
		
	def wireshark_to_hex_uncompressed(w_data):
		u_data = Futils.wireshark_to_uncompressed(w_data)
		hex_data = u_data.encode("hex")
		return hex_data
	wireshark_to_hex_uncompressed = staticmethod(wireshark_to_hex_uncompressed)
	
	def wireshark_to_wireshark_uncompressed(w_data):
		hex_data = Futils.wireshark_to_hex_uncompressed(w_data)
		w_data = Futils.hex_to_wireshark(hex_data)
		return w_data
	wireshark_to_wireshark_uncompressed = staticmethod(wireshark_to_wireshark_uncompressed)
	
	def send_mail(email_address, smtp_server, title, content):
		email = MIMEText(content)
		email['From']=email_address            
		email['To']=email_address 
		email['Subject']=title 

		server = smtplib.SMTP(smtp_server)
		server.sendmail(email_address, email_address, email.as_string()) 
		server.quit()
	
	def save_file(file, data):
		try:
			f=open(file,"a")
			f.write(str(data))
			f.close
		except IOerror as e:
			print("Futils : Impossible d'ecrire le fichier " + e)
	save_file = staticmethod(save_file)


def open_file(file):
	data = ''
	try:
		f=open(file,"r")
		data = f.read()
		f.close
	except IOerror as e :
		print("Futils : Impossible de lire le fichier " + e)
	return data

#print Futils.wireshark_to_hex_uncompressed("0" + str(3))
# print(Futils.wireshark_to_compressed('78:9c:02:db:0c:00:00:00:ff:ff'))
#print Futils.wireshark_to_wireshark_uncompressed("aabbdd")


