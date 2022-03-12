# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Input.py
# Description:		Connects input hardware to software components.
# Note:				TFMini-S MUST be configured to I2C mode over UART first.

# Imports for camera
from picamera import PiCamera
from numpy import empty, ndarray, uint8
from time import sleep
from smbus2 import SMBus, i2c_msg

class Input :

	# Class variables
	_forwardLidarAddress: int = 0x10
	_reqForwardLidar: i2c_msg = i2c_msg.write(_forwardLidarAddress, \
	[0x5A, 0x05, 0x00, 0x01, 0x60]) # Benewake TFMini-S command to read distance (cm)
	_resForwardLidar: i2c_msg = i2c_msg.read(_forwardLidarAddress, 9) # 9 result bytes

	# INITIATION FUNCTIONS

	def _initCamera(self) -> PiCamera:
		camera: PiCamera = PiCamera()
		camera.resolution = (256, 256)
		camera.framerate = 24
		sleep(2)	# Camera setup time
		return camera

	def _initForwardLidar(self) -> SMBus:
		return SMBus(1)	# Hardcoded I2C bus 1 for TESTING

	def __init__(self) -> None:
		self._camera: PiCamera = self._initCamera()
		self._forwardLidar: SMBus = self._initForwardLidar()

	# DESTRUCTION FUNCTIONS

	def _delCamera(self) -> None:
		if not (self._camera is None) :
			self._camera.close()
			self._camera = None

	def _delForwardLidar(self) -> None:
		if not (self._forwardLidar is None) :
			self._forwardLidar.close()
			self._forwardLidar = None

	def __del__(self) -> None:
		self._delCamera()
		self._delForwardLidar()

	# PUBLIC FUNCTIONS

	# Camera
	def EnableCamera(self) -> None:
		if self._camera is None :
			self._camera: PiCamera = _initCamera()

	def DisableCamera(self) -> None:
		self._delCamera()

	def GetCameraImage(self) -> ndarray:
		img: ndarray = empty((self._camera.resolution[1] * self._camera.resolution[0] * 3,), dtype=uint8)
		self._camera.capture(img, format="rgb", use_video_port=True)
		return img.reshape((self._camera.resolution[1], self._camera.resolution[0], 3))

	# Forward lidar
	def _getForwardLidarRaw(self) -> None:
		self._forwardLidar.i2c_rdwr(self._reqForwardLidar)
		sleep(0.001)
		self._forwardLidar.i2c_rdwr(self._resForwardLidar)

	def _filteredForwardLidar(self) -> int:
		self._getForwardLidarRaw()
		res: i2c_msg = self._resForwardLidar
		return (256 * int.from_bytes(res.buf[3], "big")) + int.from_bytes(res.buf[2], "big")

	def GetForwardLidar(self) -> list:
		result: int = self._filteredForwardLidar()
		if result >= 0 :
			return result
		elif result == -1 :
			raise RuntimeError("Unstable signal (strength < 100)")
		elif result == -2 :
			raise RuntimeError("Signal strength saturation")
		elif result == -4 :
			raise RuntimeError("Ambient light saturation")
		else :
			raise RuntimeError("Unknown error in LiDAR result")
