import sys
from ipcam import IPCam
from time import sleep

host_ip = '192.168.2.108'
if len(sys.argv) > 1:
	host_ip = str(sys.argv[1])

cam = IPCam(host_ip)
cam.connect()

if cam.login():
	print "Success! Connected to " + host_ip
else:
	print "Failure. Could not connect."
cam.general_info()
sleep(1)

cam.simplify_encode()
sleep(1)
cam.keep_alive()
cam.close()
