# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Input.py
# Description:		Connects input hardware to software components.

# Imports for camera
from numpy import ndarray
from system.API.modules.LiDAR import LiDAR, ForwardLiDAR, AngledLiDAR
from system.API.modules.camera import Camera

class Input :

	def close(self) -> None:
		if self._camera is not None :
			self._camera.close()
			self._camera = None
		if self._lidar_forward is not None :
			self._lidar_forward.close()
			self._lidar_forward = None
		if self._lidar_angled is not None :
			self._lidar_angled.close()
			self._lidar_angled = None

	def setActive(self) -> None:
		if self._camera is not None :
			self.setActiveCamera()
		if self._lidar_forward is not None :
			self.setActiveLidarForward()
		if self._lidar_angled is not None :
			self.setActiveLidarAngled()

	def setLowPower(self) -> None:
		if self._camera is not None :
			self.setLowPowerCamera()
		if self._lidar_forward is not None :
			self.setLowPowerLidarForward()
		if self._lidar_angled is not None :
			self.setLowPowerLidarAngled()

	def __init__(self, camera_enabled: bool = True, lidar_forward_enabled: bool = True, \
		lidar_angled_enabled: bool = True, accelerometer_enabled: bool = False) -> None:
		self._camera: Camera = None
		self._lidar_forward: LiDAR = None
		self._lidar_angled: LiDAR = None
		self._accel: LiDAR = None
		if camera_enabled :
			self._camera: Camera = Camera()
		if lidar_forward_enabled :
			self._lidar_forward: LiDAR = ForwardLiDAR()
		if lidar_angled_enabled :
			self._lidar_angled: LiDAR = AngledLiDAR()

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	# PUBLIC FUNCTIONS
	# Camera
	def setActiveCamera(self) -> None:
		self._camera.setActive()

	def setLowPowerCamera(self) -> None:
		self._camera.setLowPower()

	def GetCameraImage(self) -> ndarray:
		return self._camera.GetCameraImage()

	# Forward lidar
	def setActiveLidarForward(self) -> bool:
		return self._lidar_forward.setActive()

	def setLowPowerLidarForward(self) -> bool:
		return self._lidar_forward.setLowPower()

	def GetForwardLidar(self) -> int:
		return self._lidar_forward.GetLidar()

	# Angled lidar
	def setActiveLidarAngled(self) -> bool:
		return self._lidar_angled.setActive()

	def setLowPowerLidarAngled(self) -> bool:
		return self._lidar_angled.setLowPower()

	def GetAngledLidar(self) -> int:
		return self._lidar_angled.GetLidar()
