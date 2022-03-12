# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		LiDAR.py
# Description:		Provides functions for grabbing data from LiDAR.
# Note:				TFMini-S MUST be configured to I2C mode over UART first.

from time import sleep
from smbus2 import SMBus, i2c_msg
from enum import Enum
from typing import Dict, List

class _Addresses(Enum) :
	FORWARD = 0x10
	ANGLED = None	# Will be 0x10. Forward address will be modified

class LiDAR :

	# Request/Response i2c messages
	# Forward LiDAR
	_reqForwardLidar: i2c_msg = i2c_msg.write(_Addresses.FORWARD.value, \
		[0x5A, 0x05, 0x00, 0x01, 0x60]) # Benewake TFMini-S command to read distance (cm)
	_resForwardLidar: i2c_msg = i2c_msg.read(_Addresses.FORWARD.value, 9) # 9 result bytes
	# Angled LiDAR
	# _reqAngledLidar: i2c_msg = i2c_msg.write(_Addresses.ANGLED.value, \
	# 	[0x5A, 0x05, 0x00, 0x01, 0x60]) # Benewake TFMini-S command to read distance (cm)
	# _resAngledLidar: i2c_msg = i2c_msg.read(_Addresses.ANGLED.value, 9) # 9 result bytes

	_AddressMsgMap: Dict[_Addresses, List[i2c_msg]] = \
		{
			_Addresses.FORWARD : [_reqForwardLidar, _resForwardLidar]
		}

	def __init__(self, bus: SMBus) :
		self._bus: SMBus = bus

	def _getLidar(self, lidar: _Addresses) -> int:
		# Send request/response
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][0])
		sleep(0.001)	# Recommended wait time for result
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][1])
		# Filter result for distance
		res: i2c_msg = self._AddressMsgMap[lidar][1]
		return (256 * int.from_bytes(res.buf[3], "big")) + int.from_bytes(res.buf[2], "big")

	def _GetLidar(self, lidar: _Addresses) -> int:
		result: int = self._getLidar(lidar)
		if result >= 0 :
			return result
		elif result == -1 :
			raise RuntimeError(lidar.name + " Unstable signal (strength < 100)")
		elif result == -2 :
			raise RuntimeError(lidar.name + " Signal strength saturation")
		elif result == -4 :
			raise RuntimeError(lidar.name + " Ambient light saturation")
		else :
			raise RuntimeError(lidar.name + " Unknown error in LiDAR result")

	def GetForwardLidar(self) -> int:
		return self._GetLidar(_Addresses.FORWARD)

	def GetAngledLidar(self) -> int:
		raise NotImplementedError("Angled LiDAR address has not yet been set.")
		# return self._GetLidar(_Addresses.ANGLED)
