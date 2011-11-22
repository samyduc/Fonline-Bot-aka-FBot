from Fnet import *
from Futils import *
import sys
import os
import binascii
import threading
import time
from datetime import datetime

# connect
h_login = 'aa015abd'
len_login = 382
len_login_field = 60
pos_login_username = 20
pos_login_password = 88
# connect 2
msg_login_2 = 'aa7c5abd'

msg_login = 'aa015abd80f0c91a182a7468756e6465723100000000000000000000000000000000000000000000e823021e6c6f6c776f72000000000000000000000000000000000000000000000000656e676c085cfeb6e46fab3b1ae2b9db86d4490aa5b4716394ea1be6195e2eca1683e7ea208fafa4fe63c6d38d5bda245206028038712528ff7fbfffdb4cf9d129012b1824965294c1c270f262631a156492883f070f37f369a5966acb9e0ffd748b22738e9a3ac2de5a8864cc4ce57e014c73a249'

# antialt
pos_antialt_keyH = 	12
len_antialt_keyH = 8

pos_antialt_keyL = 	80
len_antialt_keyL = 8

pos_antialt_key1 = 88 + pos_login_password + len_login_field
len_antialt_key1 = 8

pos_antialt_key2 = pos_antialt_key1 + 24
len_antialt_key2 = 8

pos_antialt_key3 = pos_antialt_key1 + 128
len_antialt_key3 = 8

# ping pong for away
h_ping = '02'
len_ping = 16
msg_pong = 'aa055abd02'

h_ping2 = '5a'
len_ping2 = 22

def searchForPing(data):
	if(len(data) > 150):
			return False
	data = data.replace("000000ffff", "000000ffff ")
	packetList = data.split(" ")
	for packet in packetList:
		if(packet[:2] == h_ping and len(packet) < 30):
			print packet
			return True
		elif(packet[:2] == h_ping2 and len(packet) == len_ping2):
			print packet
			return True
	return False

# item id
grab_ironore_id = 6146
grab_mineral_id = 41509
grab_atelier_id = 157

drop_mineral_id = 1121436163
drop_metalpart_id = 4044958725
drop_gunpowder_id = 1797532677


craft_metalpart_id = 123
craft_gunpowder_id = 124
	
# punch
msg_punch = 'aa555abd0300000000e8030002ca200000000000000000'
pos_punch_id = 26
len_punch_id = 4

# first aid
msg_first_aid = 'aa565abdce0002a12900000000aa055abd01'
pos_first_aid_id = 14
len_first_aid_id = 4

# grab
msg_grab = 'aa525abd4e004500a225'
pos_pos_item_grab = 8
len_pos_item_grab = 4
pos_id_item_grab = 16
len_id_item_grab = 4

# drop
msg_drop = 'aa515abd0142d7c20300ff0c000000'
pos_id_item_drop = 10
len_id_item_drop  = 8
pos_nb_item_drop = 22
len_nb_item_drop = 8

# craft
msg_craft = 'aa3e5abd7c000000aa055abd01'
pos_id_item_craft = 8
len_id_item_craft  = 8

# craft 2
# still raw packet wtf ???
msg_craft2 = 'aa3d5abdbe0000002d0001000000020000000c0000001b000000200000002f000000370000003d0000003e0000003f00000041000000440000004b0000004f0000005100000052000000530000005400000055000000560000005700000058000000590000005a0000005b000000650000006700000072000000730000007400000075000000760000007700000078000000790000007a0000007b0000007c0000007d0000007d0000007e0000007f000000800000008100000084000000'

# move
msg_move = 'aa2c5abdfcff51004200'

# rotate
msg_rotate = 'aa295abd01'
pos_rotation_rotate = 9


def display(message):
	print (str(datetime.now()) + message)

def connect_msg_1(Fconfig):
	hex_data = msg_login
	temp = hex_data[:pos_antialt_keyH] + Fconfig.msg_antialt_keyH
	temp = temp + hex_data[pos_antialt_keyH+len_antialt_keyH:pos_login_username] + Futils.string_to_encode(Fconfig.login_username, len_login_field)
	temp = temp + hex_data[pos_login_username+len_login_field:pos_antialt_keyL] + Fconfig.msg_antialt_keyL
	temp = temp + hex_data[pos_antialt_keyL+len_antialt_keyL:pos_login_password] + Futils.string_to_encode(Fconfig.login_password, len_login_field)
	temp = temp + hex_data[pos_login_password+len_login_field:pos_antialt_key1] + Fconfig.msg_antialt_key1
	temp = temp + hex_data[pos_antialt_key1+len_antialt_key1:pos_antialt_key2] + Fconfig.msg_antialt_key2
	temp = temp + hex_data[pos_antialt_key2+len_antialt_key2:pos_antialt_key3] + Fconfig.msg_antialt_key3
	temp = temp + hex_data[pos_antialt_key3+len_antialt_key3:]
	return temp
	
def punch(aim_id):
	hex_data = msg_punch
	temp = hex_data[:pos_punch_id] + hex(aim_id)[4:6] + hex(aim_id)[2:4]
	temp = temp + hex_data[pos_punch_id+len_punch_id:]
	return temp
	
def first_aid(aim_id):
	hex_data = msg_first_aid
	temp = hex_data[:pos_first_aid_id] + hex(aim_id)[4:6] + hex(aim_id)[2:4]
	temp = temp + hex_data[pos_first_aid_id+len_first_aid_id:]
	return temp
	
def grab(pos_item, item_id):
	hex_data = msg_grab
	# append position 
	# note : pos is a tuple of 2 elements
	temp = hex_data[:pos_pos_item_grab] + Futils.int_to_encode(pos_item[0], len_pos_item_grab)
	temp = temp + Futils.int_to_encode(pos_item[1], len_pos_item_grab)
	# append item id
	temp = temp + hex(item_id)[2:]
	return temp
	
def drop(nb_item, item_id):
	hex_data = msg_drop
	temp = hex_data[:pos_id_item_drop] + Futils.int_to_encode(item_id, len_id_item_drop)
	temp = temp + hex_data[pos_id_item_drop+len_id_item_drop:pos_nb_item_drop]
	temp = temp + Futils.int_to_encode(nb_item, len_nb_item_drop)
	print(temp)
	return temp
	
def craft(item_id):
	hex_data = msg_craft
	temp = hex_data[:pos_id_item_craft] + Futils.int_to_encode(item_id, len_id_item_craft)
	temp = temp + hex_data[pos_id_item_craft + len_id_item_craft:]
	print(temp)
	return temp
	
def craft2():
	hex_data = msg_craft2
	temp = hex_data
	return temp
	
def move():
	hex_data = msg_move
	temp = hex_data
	return temp
	
def rotate(rotation):
	hex_data = msg_rotate
	temp = hex_data[:pos_rotation_rotate]
	temp = temp + hex(rotation)[2:]
	
	return temp

class Faction:
	def __init__(self, name, hex_msg, time, next_state=''):
		self.name = name
		self.hex_msg = hex_msg
		self.time = time
		self.next_state = next_state
		
class Fstate:
	def __init__(self, repeat=True):
		self.action = []
		self.repeat = repeat

class Fbot(threading.Thread):
	def __init__(self, Fconfig):
		threading.Thread.__init__(self)
		self.semBuf = threading.BoundedSemaphore(1)
		self.config = Fconfig
		self.running = True
		
		self.pingCount = 0
		
		# init action and state here
		self.current_state = 'login'
		self.default_state = 'action'
		self.state = {}
		self.state['login'] = Fstate(False)
		self.state['login'].action.append(Faction('send login and password with hw key', connect_msg_1(self.config), 1))
		self.state['login'].action.append(Faction('login confirm', msg_login_2, 3))
		self.state['login'].action.append(Faction('tempo', '', 2, 'action'))
		
		self.state['action'] = Fstate(True)
		self.state['action'].action.append(Faction('nothing', '', 5))
		#self.state['action'].action.append(Faction('grab', grab((81,73), grab_mineral_id), 5))
		#self.state['action'].action.append(Faction('drop', drop(3, drop_mineral_id), 5))
		
		#self.state['action'].action.append(Faction('move', move(), 5))
		#self.state['action'].action.append(Faction('rotate', rotate(1), 5))
		#self.state['action'].action.append(Faction('grab raw', grab((80,66), grab_ironore_id), 5))
		#self.state['action'].action.append(Faction('grab raw', grab((80,66), grab_mineral_id), 5))
		#self.state['action'].action.append(Faction('rotate', rotate(5), 5))
		self.state['action'].action.append(Faction('grab', grab((81,65), grab_atelier_id), 5))
		#self.state['action'].action.append(Faction('craft', craft2(), 5))
		#self.state['action'].action.append(Faction('gunpowder', craft(craft_gunpowder_id), 5))
		self.state['action'].action.append(Faction('metalpart', craft(craft_metalpart_id), 5))
		#self.state['action'].action.append(Faction('drop gunpowder', drop(1, drop_gunpowder_id), 5))
		#self.state['action'].action.append(Faction('drop metalpart', drop(1, drop_metalpart_id), 5))
		
		
		self.buffer = ''
		self.net = Fnet(self, self.config)
		self.socketThread = SocketThread()
		self.socketThread.start()
		
	def run(self):
		display('....Starting....')
		display('....Starring : ' + self.config.login_username)
		while(self.running):
			isBreak = False
			for action in self.state[self.current_state].action:
				if (not self.running):
					break;
				display('....Action : ' + action.name)
				self.send(action.hex_msg)
				if(action.next_state != ''):
					isBreak = True
					self.current_state = action.next_state
					break
				time.sleep(action.time)
					
			if(self.state[self.current_state].repeat == False and isBreak == False):
				self.current_state = self.default_state
				display('....Switching to default action : ' + self.default_state)
			
	def isRunning(self):
		return self.running
			
	def handle(self, hex_data):
		if (searchForPing(hex_data)):
			self.send(msg_pong)
			self.pingCount = self.pingCount + 1
			display('....Pong....')
			
	# need to be tested
	def send(self, hex_data):
		pending = True
		while(pending):
			self.semBuf.acquire()
			if(self.buffer == ''):
				self.buffer = binascii.unhexlify(hex_data)
				pending = False
			self.semBuf.release()
			time.sleep(0.001)
		
	def send_to_Fnet(self):
		time.sleep(0.001)
		self.semBuf.acquire()
		temp = self.buffer
		self.buffer = ''
		self.semBuf.release()
		return temp
		