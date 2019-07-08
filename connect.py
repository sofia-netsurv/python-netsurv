import sys
from dvrip import DVRIPCam
from time import sleep

if len(sys.argv) > 1:
	if str(sys.argv[1] == 'interactive'):
		host_ip = input()
	else:
		host_ip = str(sys.argv[1])
else:
	host_ip = '192.168.1.156'

cam = DVRIPCam(host_ip)
cam.connect()
if cam.login():
	print({"command" : "connect", "success" : True });

	while True:
		command = input()

		if command == "status":
			print({"command" : "status", "success" : True, "response" : "connected" });
	
else:	
	print({"command" : "connect", "success" : False});


# if cam.login():
# 	print("Success! Connected to " + host_ip)
# else:
# 	print("Failure. Could not connect.")

# 	enc_info = cam.get_info(1042, "Simplify.Encode")

# 	cam.get_system_info()
# 	sleep(1)
# 	cam.get_camera_info()
# 	sleep(1)

# 	enc_info['Simplify.Encode'][0]['ExtraFormat']['Video']['FPS'] = 20
# 	cam.set_info(1040, "Simplify.Encode", enc_info)
# 	sleep(2)
# 	print(cam.get_info(1042, "Simplify.Encode"))
# 	cam.close()
