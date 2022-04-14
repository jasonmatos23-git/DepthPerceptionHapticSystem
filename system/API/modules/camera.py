# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		camera.py
# Description:		Provides camera functionality.

from picamera import PiCamera
from numpy import empty, ndarray, uint8
from time import sleep

class Camera :

	def setActive(self) -> None:
		if self._camera is None :
			self.__init__()

	def setLowPower(self) -> None:
		self.close()

	def close(self) -> None:
		pass
		# if self._camera is not None :
		# 	self._camera.close()
		# 	self._camera = None

	def __init__(self) -> None:
		self._camera: PiCamera = PiCamera()
		self._camera.resolution = (256, 256)	# Input tensor shape is (1,256,256,3)
		self._camera.rotation = 90
		self._camera.framerate = 24
		sleep(2)	# Camera setup time

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	def GetCameraImage(self) -> ndarray:
		if self._camera is None :
			raise RuntimeError("Camera is not enabled.")
		img: ndarray = empty((self._camera.resolution[1] * self._camera.resolution[0] * 3,), dtype=uint8)
		self._camera.capture(img, format="rgb", use_video_port=True)
		return img.reshape((self._camera.resolution[1], self._camera.resolution[0], 3))
