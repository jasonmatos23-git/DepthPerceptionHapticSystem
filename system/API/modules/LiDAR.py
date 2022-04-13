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
	ANGLED = 0x11	

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

	# Low power consumption mode i2c messages
	# Forward LiDAR
	_reqLowPowerForward: i2c_msg = i2c_msg.write(_Addresses.FORWARD.value, \
		[0x5A, 0x06, 0x35, 0x01, 0x00, 0x96]) # Set low power mode (X ranges 0 - A, freq <= 10 Hz)
	_resLowPowerForward: i2c_msg = i2c_msg.read(_Addresses.FORWARD.value, 6) # 6 result bytes
	_reqNormalPowerForward: i2c_msg = i2c_msg.write(_Addresses.FORWARD.value, \
		[0x5A, 0x06, 0x35, 0x00, 0x00, 0x95]) # Set normal
	_resNormalPowerForward: i2c_msg = i2c_msg.read(_Addresses.FORWARD.value, 6) # 6 result bytes
	# Angled LiDAR
	# _reqLowPowerAngled: i2c_msg = i2c_msg.write(_Addresses.ANGLED.value, \
	# 	[0x5A, 0x06, 0x35, 0x01, 0x00, 0x96]) # Set low power mode (frequency must be <= 10 Hz)
	# _resLowPowerAngled: i2c_msg = i2c_msg.read(_Addresses.ANGLED.value, 6) # 6 result bytes
	# _reqNormalPowerAngled: i2c_msg = i2c_msg.write(_Addresses.ANGLED.value, \
	# 	[0x5A, 0x06, 0x35, 0x00, 0x00, 0x95]) # Set normal
	# _resNormalPowerAngled: i2c_msg = i2c_msg.read(_Addresses.ANGLED.value, 6) # 6 result bytes

	_AddressMsgMap: Dict[_Addresses, List[i2c_msg]] = \
		{
			_Addresses.FORWARD : [ \
				_reqForwardLidar, _resForwardLidar, \
				_reqLowPowerForward, _resLowPowerForward, \
				_reqNormalPowerForward, _resNormalPowerForward]
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

	def _setNormalPower(self, lidar: _Addresses) -> bool:
		# Send request/response
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][4])
		sleep(0.001)	# Recommended wait time for result
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][5])
		# Compare response
		return self._AddressMsgMap[lidar][4].buf[3] == self._AddressMsgMap[lidar][5].buf[3]

	def _setLowPower(self, lidar: _Addresses) -> bool:
		# Send request/response
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][2])
		sleep(0.001)	# Recommended wait time for result
		self._bus.i2c_rdwr(self._AddressMsgMap[lidar][3])
		# Compare response
		return self._AddressMsgMap[lidar][3].buf[3] == self._AddressMsgMap[lidar][2].buf[3]

	def setLowPowerForward(self) -> bool:
		return self._setLowPower(_Addresses.FORWARD)

	def setLowPowerAngled(self) -> bool:
		raise NotImplementedError("Angled LiDAR address has not yet been set.")
		# return self._setLowPower(_Addresses.ANGLED)

	def setNormalPowerForward(self) -> bool:
		return self._setNormalPower(_Addresses.FORWARD)

	def setNormalPowerAngled(self) -> bool:
		raise NotImplementedError("Angled LiDAR address has not yet been set.")
		# return self._setNormalPower(_Addresses.ANGLED)

	def setNormalPower(self) -> bool:
		# 'and' used since dangerous if one lidar
		# does not return from LPM
		return setNormalPowerAngled() and setNormalPowerForward()

	def setLowPower(self) -> bool:
		return setLowPowerAngled() or setLowPowerForward()
