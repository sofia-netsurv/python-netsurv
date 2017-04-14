import sys
from dvrip import DVRIPCam
from time import sleep

host_ip = '192.168.2.108'
if len(sys.argv) > 1:
	host_ip = str(sys.argv[1])

cam = DVRIPCam(host_ip)
cam.connect()

if cam.login():
	print "Success! Connected to " + host_ip
else:
	print "Failure. Could not connect."
cam.get_camera_info()
sleep(1)
cam.get_camera_info(True)
sleep(1)
cam.get_system_info()

cam.close()
