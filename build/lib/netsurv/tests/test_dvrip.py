from dvrip import DVRIPCam


def test_init():
    cam = DVRIPCam("192.168.1.10")
    assert cam
