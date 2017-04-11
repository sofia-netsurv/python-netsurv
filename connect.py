#!/usr/bin/env python
import json
import socket
import binascii
import sys


class Sofia(object):
	def __init__(self):
		pass


class IPCam(object):
	def __init__(self, user="admin", password= "tlJwpbo6"):
		pass





def bytes(integer):
	return divmod(integer, 0x100)

def send_packet(host_socket, msg):	
	host_socket.send(msg)

	data = host_socket.recv(1024)
	return data

def connect_to_host(tcp_ip, tcp_port = 34567):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((tcp_ip, tcp_port))
	
	return s
def build_packet(input_data, message_code, encoding = "ascii"):
	
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
	sequence_number = "\x00"     #Number of packets sent in current session
	unknown_block_1 = "\x00\x00\x00\x00\x00"
	message_byte_1 = chr(low)  	#message code from definition table, little-endian order
	message_byte_2 = chr(high)

	
	data_len = chr(len(data)+1) +"\x00\x00\x00" #Size of data in bytes (padded to 2 bytes)
	data = data + "\x0a"	#ascii data, maximum of 16kb, terminated with a null ascii character
	
	packet = head_flag + version + reserved_01 + reserved_02 + session_id + unknown_block_0 + sequence_number + unknown_block_1 + message_byte_1 + message_byte_2 + data_len + data
	return packet 
		
if len(sys.argv) > 1:
	host_ip = str(sys.argv[1])
else:
	host_ip = '192.168.2.108'


login_creds_struct = { "EncryptType" : "MD5", "LoginType" : "DVRIP-Web", "PassWord" : "tlJwpbo6", "UserName" : "admin" }

msg = build_packet(login_creds_struct, 1000, "struct")

s = connect_to_host(host_ip)

data = send_packet(s, msg)

parsed = data[20:].replace(" ", "")

#print "received data:", parsed[:-2]

 
parsed_json = json.loads(parsed[:-2])
session_id = parsed_json["SessionID"]
response_code = parsed_json["Ret"]

if response_code == 100:
	print "Successfully connected to device at " + host_ip
else:
	print "Device returned error:"
	print response_code
s.close()
