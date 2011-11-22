#from GUI import *
from Fbot import *
import time

tor_socks_ip = 'localhost'
tor_socks_port = 9050

class Fconfig:
	server_ip = '94.23.237.127'
	server_port = 2238

	# no proxy is empty string
	proxy_socks4_ip = ''
	proxy_socks4_port = tor_socks_port
	
	msg_antialt_keyH = 'xxxxxxxx'
	msg_antialt_keyL = 'xxxxxxxx'
	msg_antialt_key1 = 'xxxxxxxx'
	msg_antialt_key2 = 'xxxxxxxx'
	msg_antialt_key3 = 'xxxxxxxx'
	
	login_id = 13129
	login_username = 'Gretchen'
	login_password = 'xxxxxxxx'
	target_id = 8394
	
	number_of_punch = 65
	time_to_heal = 130
	
# def poll():
	# gui.after(200, poll)
	# gui.refresh()
	
# if __name__ == '__main__':
	# gui = GUI(Fconfig)
	# poll()
	# gui.mainloop()
	# gui.clean()
	
if __name__ == '__main__':
	while(True):
		bot = Fbot(Fconfig)
		while(bot.isRunning()):
			time.sleep(1)
		bot.join()
		time.sleep(10)
