import sys
from ipcam import IPCam

host_ip = '192.168.2.108'
if len(sys.argv) > 1:
	host_ip = str(sys.argv[1])

cam = IPCam(host_ip)
cam.connect()
cam.login()
cam.close()
