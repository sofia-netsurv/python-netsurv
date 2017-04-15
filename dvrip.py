#!/usr/bin/env python
import json
import socket
import binascii
import sys
from codes import check_response_code, lookup_response_code



def bytes(integer):
	return divmod(integer, 0x100)

class DVRIPCam(object):
	def __init__(self, tcp_ip, user="admin", password= "tlJwpbo6", auth = "MD5", tcp_port = 34567):
		self.tcp_ip = tcp_ip	
		self.user = user
		self.password = password
		self.tcp_port = 34567
		self.auth = auth
		self.socket = None
		self.packet_count = 0
		self.session_int = 0
		self.session_hex = None
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.tcp_ip, self.tcp_port))
		
	def close(self):
		self.socket.close()
	def send_packet(self, msg):	
		self.socket.send(msg)
		data = self.socket.recv(5012+5012)
		return data
	def clean_response(self, data):
		
		cleaned = data[20:].replace(" ", "")
		cleaned = cleaned[:-2]
		return cleaned	
	def build_packet(self, input_data, message_code, encoding = "ascii"):
		
		if encoding == "hex":
			data = binascii.unhexlify(input_data)

		elif encoding == "ascii":
			data = input_data
		elif encoding == "struct":
			data = json.dumps(input_data)


		high, low = bytes(message_code)
		
		#structure of control flow message packet per spec
		head_flag = "\xFF" 	#One byte fixed value of 0xFF
		version = "\x00" 	#Version number, currently
		reserved_01 = "\x00"	#Reserved, fixed value of 0x00
		reserved_02 = "\x00"	
		session_id = "\x00" 	#Session id, default 0i
		unknown_block_0 = "\x00\x00\x00"
		sequence_number = chr(self.packet_count)     #Number of packets sent in current session
		unknown_block_1 = "\x00\x00\x00\x00\x00"
		message_byte_1 = chr(low)  	#message code from definition table, little-endian order
		message_byte_2 = chr(high)

		
		data_len = chr(len(data)+1) +"\x00\x00\x00" #Size of data in bytes (padded to 2 bytes)
		data = data + "\x0a"	#ascii data, maximum of 16kb, terminated with a null ascii character
		
		packet = head_flag + version + reserved_01 + reserved_02 + session_id + unknown_block_0 + sequence_number + unknown_block_1 + message_byte_1 + message_byte_2 + data_len + data
		return packet 
	def send(self, input_data, message_code, encoding = "ascii"):
		packet = self.build_packet(input_data, message_code, encoding)
		self.packet_count += 1

		return json.loads(self.clean_response(self.send_packet(packet)))
	def login(self):	
		login_creds_struct = { "EncryptType" : self.auth, "LoginType" : "DVRIP-Web", "PassWord" : self.password, "UserName" : self.user }
		data = self.send(login_creds_struct, 1000, "struct")

		parsed_json = data

		self.session_id_hex = parsed_json["SessionID"]
		response_code = parsed_json["Ret"]

		if check_response_code(response_code):
			return True
		else:
			return False

	def pretty_print(self, data):
		print json.dumps(data, indent = 4, sort_keys = True)		

	def keep_alive(self):
		message_struct = {"Name" : "KeepAlive", "SessionID" :self.session_id_hex}
		data = self.send(message_struct, 1006, "struct")
		self.pretty_print(data)

	def get_info(self, code, command):
		info_struct = {"Name" : str(command), "SessionID" : self.session_id_hex}
		data = self.send(info_struct, code, "struct")
		return data
	
	def get_system_info(self):
		data = self.get_info("General", 1042)
			
		self.pretty_print(data)
		
	def get_encode_capabilities(self):
		data = self.get_info(1360, "EncodeCapability")
		self.pretty_print(data)
	
	def get_system_capabilities(self):
		data = self.get_info(1360, "SystemFunction")
		self.pretty_print(data)
	
	def get_camera_info(self, default = False):
		"""Request data for 'Camera' from  the target DVRIP device."""
		if default:
			code = 1044
		else:
			code = 1042
		data = self.get_info(code, "Camera")
		self.pretty_print(data)
		
	def get_encode_info(self, default = False):
		"""Request data for 'Simplify.Encode' from the target DVRIP device.

			Arguments:
			default -- returns the default values for the type if True

		"""

		if default:
			code = 1044
		else:
			code = 1042

		data = self.get_info(code, "Simplify.Encode")
		self.pretty_print(data)
