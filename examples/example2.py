import sys
from netsurv import DVRIPCam
from time import sleep
import json

if len(sys.argv) > 1:
    if str(sys.argv[1] == 'interactive'):
        host_ip = input()
    else:
        host_ip = str(sys.argv[1])
else:
    host_ip = '192.168.1.139'

cam = DVRIPCam(host_ip)
if cam.connect():
    if cam.login():
        print(json.dumps({"command": "connect", "success": True}))

        while True:
            command = input()

            if command == "status":
                print(json.dumps({"command": "status",
                                  "success": True, "response": "connected"}))

    else:
        print(json.dumps({"command": "connect", "success": False}))
    cam.close()
