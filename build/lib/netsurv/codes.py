error_codes = {
	"101" : "Unknown error",
	"102" : "Unsupported version",
	"103" : "Request not permitted",
	"104" : "User already logged in",
	"105" : "User is not logged in",
	"106" : "Username or password is incorrect",
	"107" : "User does not have necessary permissions",
	"203" : "Password is incorrect"
}
success_codes = {
	"100" : "OK",
	"515" : "Upgrade successful"
}

command_codes = {
	"KeepAlive" :	1006,
	"General"	:	1042,
	"EncodeCapability"	:	1360,
	"SystemFunction"	:	1360,
	"Camera"	:	1042,			# Request data for 'Camera' from  the target DVRIP device.
	"Simplify.Encode"	:	1042	# Request data for 'Simplify.Encode' from the target DVRIP device.
}

def check_response_code(code):
	code = str(code)

	if code in success_codes:
		return True
	else:
		return False

def lookup_response_code(code):
	code = str(code)
	if code in error_codes:
		return error_codes[code]
	elif code in success_codes:
		return success_codes[code]

def lookup_command_code(code):
	return command_codes[code]
