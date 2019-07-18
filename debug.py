from dvrip import DVRIPCam
from time import sleep
import json

def pretty_print(data):
	print(json.dumps(data, indent = 4, sort_keys = True))

host_ip = '192.168.1.139'

cam = DVRIPCam(host_ip)
cam.connect()
if cam.login():
	print("Success! Connected to " + host_ip)
else:
 	print("Failure. Could not connect.")

enc_info = cam.get_info("Simplify.Encode")

pretty_print(cam.get_info("General"))
sleep(1)
pretty_print(cam.get_info("Camera"))
sleep(1)

enc_info['Simplify.Encode'][0]['ExtraFormat']['Video']['FPS'] = 20
cam.set_info(1040, "Simplify.Encode", enc_info)
sleep(2)
pretty_print(cam.get_info("Simplify.Encode"))
cam.close()
