import socket, asyncore
import sys
import os
import binascii
import threading
from Fbot import *

len_socks4 = 18
h_socks4 = "0401"
d_socks4 = "005a"

class SocketThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		asyncore.loop()

class Fnet(asyncore.dispatcher):
	def __init__(self, bot, Fconfig):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.config = Fconfig
		# if proxy
		if(self.config.proxy_socks4_ip != ''):
			self.connect( (self.config.proxy_socks4_ip, self.config.proxy_socks4_port) )
		else:
			self.connect( (self.config.server_ip, self.config.server_port) )
		self.buffer = ''
		self.bot = bot
		
	def handle_connect(self):
		if(self.config.proxy_socks4_ip != ''):
			# build socks packet
			# header
			hex_data = h_socks4
			# port
			hex_server_port = hex(self.config.server_port)[2:]
			hex_server_port = '0'*(4-len(hex_server_port)) + hex_server_port
			hex_data = hex_data + hex_server_port
			# host from xxx.xxx.xxx.xxx to hex
			str_host = self.config.server_ip.split('.')
			hex_host  = ''
			for host in str_host:
				int_host = int(host)
				hex_host += hex(int_host)[2:]
			hex_data = hex_data + hex_host
			hex_data = hex_data + '00'
			# send
			self.buffer = binascii.unhexlify(hex_data)
		else:
			self.bot.start()
	
	def handle_write(self):
		if(self.buffer == ''):
			self.buffer = self.bot.send_to_Fnet()
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
		
	def handle_read(self):
		hex_rcv = self.recv(1024).encode('hex')
	
		if(hex_rcv[:4] == d_socks4):
			self.bot.start()
		else:
			self.bot.handle(hex_rcv)

	def handle_close(self):
		print('....Closing....')
		self.close()
		self.bot.running = False
		self.bot.join()