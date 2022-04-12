# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		LiDAR.py
# Description:		Provides functions for grabbing data from LiDAR.
# Note:				TFMini-S MUST be configured to I2C mode over UART first.

from time import sleep
from smbus2 import SMBus, i2c_msg
from enum import Enum

# Exceptions for lidar
class LiDARException(Exception) :
	pass

class LowSignalStrength(LiDARException) :
	pass

class SignalStrengthSaturation(LiDARException) :
	pass

class AmbientLightSaturation(LiDARException) :
	pass

# LiDAR superclass
class LiDAR :

	# Request/Response i2c messages
	# Note: 0x00 is used as a PLACEHOLDER address
	# 	Overwritten in subclasses below
	# Benewake TFMini-S command to read distance (cm)
	_reqLidar: i2c_msg = i2c_msg.write(0x00, [0x5A, 0x05, 0x00, 0x01, 0x60])
	# 9 result bytes
	_resLidar: i2c_msg = i2c_msg.read(0x00, 9)

	# Power consumption mode i2c messages
	# Note: buf[5]s low-byte checksum must be updated w.r.t address in classes below
	# Set modes
	_reqNormalPower: i2c_msg = i2c_msg.write(0x00, [0x5A, 0x06, 0x35, 0x00, 0x00, 0x95])
	_reqLowPower: i2c_msg = i2c_msg.write(0x00, [0x5A, 0x06, 0x35, 0x01, 0x00, 0x96])
	# 6 result bytes
	_resPower: i2c_msg = i2c_msg.read(0x00, 6)

	# Recommended wait time for results
	_waitTime: int = 0.001

	def _getDistance(self) -> int:
		# Send request/response
		self._bus.i2c_rdwr(self._reqLidar)
		sleep(self._waitTime)	# Recommended wait time for result
		self._bus.i2c_rdwr(self._resLidar)
		# Filter result for distance
		return (256 * int.from_bytes(self._resLidar.buf[3], "big")) + \
			int.from_bytes(self._resLidar.buf[2], "big")

	def GetLidar(self) -> int:
		result: int = self._getDistance()
		if result < 65532 :
			return result
		elif result == 65535 :
			raise LowSignalStrength("LiDAR Unstable signal (strength < 100)")
		elif result == 65534 :
			raise SignalStrengthSaturation("LiDAR Signal strength saturation")
		elif result == 65532 :
			raise AmbientLightSaturation("LiDAR Ambient light saturation")

	# Returns True if active mode set
	def setActive(self) -> bool:
		if self._active :
			return True
		# Send request/response
		self._bus.i2c_rdwr(self._reqNormalPower)
		sleep(self._waitTime)
		self._bus.i2c_rdwr(self._resPower)
		# Compare buffer checksums
		self._active = self._resPower.buf[5] == self._reqNormalPower.buf[5]
		return self._active

	# Returns True if low power mode set
	def setLowPower(self) -> bool:
		if not self._active :
			return True
		# Send request/response
		self._bus.i2c_rdwr(self._reqLowPower)
		sleep(self._waitTime)
		self._bus.i2c_rdwr(self._resPower)
		# Compare buffer checksums
		self._active = not (self._resPower.buf[5] == self._reqLowPower.buf[5])
		return not self._active

	def close(self) -> None:
		if self._bus is not None :
			self.setLowPower()
			self._bus.close()
			self._bus = None
			self._active = False

	def __init__(self, bus_no: int = 1) :
		self._bus: SMBus = SMBus(bus_no)
		self._active: bool = False

	def __enter__(self) -> None:
		return self

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	def __del__(self) -> None:
		self.close()

class ForwardLiDAR(LiDAR) :

	# Request/Response i2c messages
	_reqLidar: i2c_msg = i2c_msg.write(0x10, [0x5A, 0x05, 0x00, 0x01, 0x60])
	# 9 result bytes
	_resLidar: i2c_msg = i2c_msg.read(0x10, 9)

	# Power consumption mode i2c messages
	# Set modes
	_reqNormalPower: i2c_msg = i2c_msg.write(0x10, [0x5A, 0x06, 0x35, 0x00, 0x00, 0xa5])
	_reqLowPower: i2c_msg = i2c_msg.write(0x10, [0x5A, 0x06, 0x35, 0x01, 0x00, 0xa6])
	# 6 result bytes
	_resPower: i2c_msg = i2c_msg.read(0x10, 6)

class AngledLiDAR(LiDAR) :

	# Request/Response i2c messages
	_reqLidar: i2c_msg = i2c_msg.write(0x11, [0x5A, 0x05, 0x00, 0x01, 0x60])
	# 9 result bytes
	_resLidar: i2c_msg = i2c_msg.read(0x11, 9)

	# Power consumption mode i2c messages
	# Set modes
	_reqNormalPower: i2c_msg = i2c_msg.write(0x11, [0x5A, 0x06, 0x35, 0x00, 0x00, 0xa6])
	_reqLowPower: i2c_msg = i2c_msg.write(0x11, [0x5A, 0x06, 0x35, 0x01, 0x00, 0xa7])
	# 6 result bytes
	_resPower: i2c_msg = i2c_msg.read(0x11, 6)
