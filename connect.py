#!/usr/bin/env python
import json
import socket
import binascii
import sys

def bytes(integer):
	return divmod(integer, 0x100)


def little_endian_hex_str(dec, length = 4):
	hex_str = ""
	

def build_packet(input_data, message_code, encoding = "ascii"):
	
	if encoding == "hex":
		data = binascii.unhexlify(input_data)

	elif encoding == "ascii":
		data = input_data
	elif encoding == "struct":
		data = json.dumps(data)


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
		
if len(sys.argv):
	TCP_IP = str(sys.argv[1])
else:
	TCP_IP = '192.168.2.108'
TCP_PORT = 34567
BUFFER_SIZE = 1024
login_creds = '{ "EncryptType" : "MD5", "LoginType" : "DVRIP-Web", "PassWord" : "tlJwpbo6", "UserName" : "admin" }'

MESSAGE = build_packet(login_creds, 1000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

data = s.recv(BUFFER_SIZE)
parsed = data[20:].replace(" ", "")

print "received data:", parsed[:-2]

 
parsed_json = json.loads(parsed[:-2])
session_id = parsed_json["SessionID"]
print "Session established with server:"
print session_id

s.send(MESSAGE)
s.close()
