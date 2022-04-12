# Primary Author:	Chad Pauley (chadpauley65@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		configure.py
# Description:		Holds GPIO configuration.

import pigpio
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Configuration :

	def __init__(self) :
		#Note for programming
		#Pull high/low aka up/down is only used with applications not involving
		#predesigned i/o, such as buttons

		self._pi = pigpio.pi()

		#-----------------------
		#Button Inputs

		#GPIO Pins
		self.BUTTON_PIN_6 = 6
		self.BUTTON_PIN_14 = 14
		self.BUTTON_PIN_15 = 15
		self.BUTTON_PIN_16 = 16
		self.BUTTON_PIN_17 = 17

		#May encounter error with pin 99 as it is already default at low and powers off the system by manufacturer
		#replace to pull_up_down=GPIO.PUD_UP for a pull up if needed
		GPIO.setup(self.BUTTON_PIN_6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.BUTTON_PIN_14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.BUTTON_PIN_15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.BUTTON_PIN_16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.BUTTON_PIN_17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		#-----------------------
		#Camera Pins I/O

		#These variables for camera may be unnecessary
		#No conversion needed
		# NOTE: CAM lines below have not been modified to
		# their corrected values
		self._CAM_IO1 = 24
		self._CAM_IO0 = 48
		self._CAM_SCL = 80
		self._CAM_SDA = 82
		self._CAM0_D0_N = 128
		self._CAM0_D0_P = 130
		self._CAM0_D1_N = 134
		self._CAM0_D1_P = 136
		self._CAM0_C_N = 140
		self._CAM0_C_P = 142

		#-----------------------
		#Accelerometer I/O

		#Conversion to SPI (ALT0)
		#Accel_CE1_N is an extra GPIO in case of need for bus
		self._Accel_SCL = 11	#Clock
		self._Accel_MISO = 9	#Main In
		self._Accel_MOSI = 10	#Main Out
		self._Accel_CE0_N = 8	#Chip Select 0
		self._Accel_CE1_N = 7	#Chip Select 1

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed but use code similar to below if needed
		#pi.set_mode(Accel_SCL, pigpio.ALT0)

		#-----------------------
		#Motor Controller I/O

		#Conversion to I2C (ALT0)
		self._Motor_SDA = 2
		self._Motor_SCL = 3

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed

		#-----------------------
		#Lidar 1 I/O

		#Conversion to I2C (ALT0)
		self._Lidar_1_SCL = 1
		self._Lidar_1_SDA = 0

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed

		#-----------------------
		#Lidar 2 I/O

		#Conversion to I2C (ALT5)
		self._Lidar_2_SCL = 5
		self._Lidar_2_SDA = 4

		#Setting to ALT5 configuration
		self._pi.set_mode(self._Lidar_2_SCL, pigpio.ALT5)
		self._pi.set_mode(self._Lidar_2_SDA, pigpio.ALT5)

		#-----------------------
		#Speaker Output

		#Conversion to PWM (ALT0)
		self._Speaker0 = 12

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed

	def close(self) -> None:
		if self._pi is not None :
			self._pi.stop()
			GPIO.cleanup()
			self._pi = None

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()
