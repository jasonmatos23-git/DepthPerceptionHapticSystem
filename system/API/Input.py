# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Input.py
# Description:		Connects input hardware to software components.

# Imports for camera
from picamera import PiCamera
from numpy import empty, ndarray, uint8
from time import sleep

class Input :

	# INITIATION FUNCTIONS

	def _initCamera(self) -> PiCamera:
		camera: PiCamera = PiCamera()
		camera.resolution = (640, 480)
		camera.framerate = 24
		sleep(2)	# Camera setup time
		return camera

	def __init__(self) :
		self._camera: PiCamera = self._initCamera()

	# DESTRUCTION FUNCTIONS

	def _delCamera(self) :
		if not (self._camera is None) :
			self._camera.close()
			self._camera = None

	def __del__(self) :
		self._delCamera()

	# PUBLIC FUNCTIONS

	def EnableCamera(self) :
		if self._camera is None :
			self._camera = _initCamera()

	def DisableCamera(self) :
		self._delCamera()

	def GetCameraImage(self) -> ndarray:
		img: ndarray = empty((480 * 640 * 3,), dtype=uint8)
		self._camera.capture(img, format="rgb", use_video_port=True)
		return img
