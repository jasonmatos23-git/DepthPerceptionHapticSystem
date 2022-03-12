# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Input.py
# Description:		Connects input hardware to software components.

# Imports for camera
from numpy import ndarray
from smbus2 import SMBus
from system.API.modules.LiDAR import LiDAR
from system.API.modules.camera import Camera

class Input :

	def __init__(self, bus: SMBus) -> None:
		self._camera: Camera = Camera()
		self._lidar: LiDAR = LiDAR(bus)

	def __del__(self) -> None:
		del(self._camera)
		del(self._lidar)

	# PUBLIC FUNCTIONS
	# Camera
	def EnableCamera(self) -> None:
		self._camera.Enable()

	def DisableCamera(self) -> None:
		self._camera.Disable()

	def GetCameraImage(self) -> ndarray:
		return self._camera.GetCameraImage()

	# Lidar
	def GetForwardLidar(self) -> int:
		return self._lidar.GetForwardLidar()

	def GetAngledLidar(self) -> int:
		return self._lidar.GetAngledLidar()
