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
		self.BUTTON_PIN_99 = 99
		self.BUTTON_PIN_55 = 55
		self.BUTTON_PIN_51 = 51

		#May encounter error with pin 99 as it is already default at low and powers off the system by manufacturer
		#replace to pull_up_down=GPIO.PUD_UP for a pull up if needed
		GPIO.setup(self.BUTTON_PIN_99, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.BUTTON_PIN_55, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.BUTTON_PIN_51, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		#-----------------------
		#Camera Pins I/O

		#These variables for camera may be unnecessary
		#No conversion needed
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
		self._Accel_SCL = 38	#Clock
		self._Accel_MIS0 = 40	#Main Out
		self._Accel_MOS1 = 44	#Main In
		self._Accel_CE0_N = 39	#Chip Select 0
		self._Accel_CE1_N = 37	#Chip Select 1

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed but use code similar to below if needed
		#pi.set_mode(Accel_SCL, pigpio.ALT0)

		#-----------------------
		#Motor Controller I/O

		#Conversion to I2C (ALT0)
		self._Motor_SDA = 58
		self._Motor_SCL = 56

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed

		#-----------------------
		#Lidar 1 I/O

		#Conversion to I2C (ALT0)
		self._Lidar_1_SCL = 35
		self._Lidar_1_SDA = 36

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed

		#-----------------------
		#Lidar 2 I/O

		#Conversion to I2C (ALT5)
		self._Lidar_2_SCL = 34
		self._Lidar_2_SDA = 54

		#Setting to ALT5 configuration
		self._pi.set_mode(self._Lidar_2_SCL, pigpio.ALT5)
		self._pi.set_mode(self._Lidar_2_SDA, pigpio.ALT5)

		#-----------------------
		#Speaker Output

		#Conversion to PWM (ALT0)
		self._Speaker0 = 31

		#Setting to ALT0 configuration
		#ALT0 is default so code not needed
