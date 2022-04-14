# System imports
from system.system import *
from system.configure import *
from system.hardware_interrupt import *
from system.routine_container import *
from system.service_container import *
from system.scheduler import *
from system.mode import *

# API imports
from system.API.Input import *
from system.API.Output import *
from system.API.modules.speaker import *
from system.API.modules.LiDAR import *
from system.API.modules.PWM import *
from system.API.modules.camera import *

# Service imports
from system.services.depth_perception_service import *
from system.services.distanceservice import *

# Routine imports
from system.routines.depth_perception_routine import *
from system.routines.button_response import *
from system.routines.emergency_response import *
from system.routines.linear_distance_routine import *

# Mode imports
from system.modes.general import *
from system.modes.lowpower import *
from system.modes.outdoor import *

# Helper imports
from time import sleep
import numpy as np
import cv2
import subprocess

class Testbench :

	def close(self) :
		if self.config is not None :
			self.config.close()
			self.config = None

	def __init__(self) :
		self.config = Configuration()
		print("Testbench ready")

	def __enter__(self) :
		return self

	def __del__(self) :
		self.close()

	def __exit__(self) :
		self.close()

	# Component tests

	def testMotorControl_Individual(self, val = 4095, delay = 1) :
		pwm = PWM()
		for enum in Motor :
			pwm.setDutyCycle(enum, val)
			sleep(delay)
			pwm.setDutyCycle(enum, 0)
		pwm.close()

	def testMotorControl_Group(self, val = 4095, delay = 1) :
		pwm = PWM()
		pwm.setAllDutyCycle(val)
		sleep(delay)
		pwm.setAllDutyCycle(0)

	def testMotorControl_Step(self, val = 3, delay = 1, index = 0) :
		pwm = PWM()
		for i in range(val + 1, 1, -1) :
			pwm.setDutyCycle(index, int(4095.0/i))
			sleep(delay)
		pwm.close()

	def testSpeaker_Connectivity(self, val = 10000) :
		speak = Speaker()
		speak.setVolume(val)
		speak.playPattern(Audio.TEMPLATE_TUNE.value)
		speak.close()

	def testCamera_Connectivity(self) :
		cam = Camera()
		im = cam.GetCameraImage()
		cv2.imwrite("cameraConnectivityTest.jpg", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
		cam.close()

	def testLidar_Forward(self, delay = 1) :
		fl = ForwardLiDAR()
		try :
			while True :
				try :
					print(fl.GetLidar() * 0.03281)
				except LiDARException as e :
					print("LiDAR Exception detected: " + str(type(e).__name__))
				sleep(delay)
		except KeyboardInterrupt :
			pass
		fl.close()

	def testLidar_Angled(self, delay = 1) :
		al = AngledLiDAR()
		try :
			while True :
				try :
					print(al.GetLidar() * 0.03281)
				except LiDARException as e :
					print("LiDAR Exception detected: " + str(type(e).__name__))
				sleep(delay)
		except KeyboardInterrupt :
			pass
		al.close()

	def _buttonValidation(self, channel) :
		print("Button press registered")

	def testButtons_Individual(self, val = 6) :
		if val not in [6, 14, 15, 16, 17] :
			print("INVALID input argument")
			return
		hi = HardwareInterrupt()
		if val == 6 :
			hi.setCallback(hi.conf.BUTTON_PIN_6, self._buttonValidation)
		elif val == 14 :
			hi.setCallback(hi.conf.BUTTON_PIN_14, self._buttonValidation)
		elif val == 15 :
			hi.setCallback(hi.conf.BUTTON_PIN_15, self._buttonValidation)
		elif val == 16 :
			hi.setCallback(hi.conf.BUTTON_PIN_16, self._buttonValidation)
		elif val == 17 :
			hi.setCallback(hi.conf.BUTTON_PIN_17, self._buttonValidation)
		try :
			while True :
				sleep(60)
		except KeyboardInterrupt :
			pass
		hi.close()

	def testButtons_Group(self) :
		hi = HardwareInterrupt()
		hi.setCallback(hi.conf.BUTTON_PIN_6, self._buttonValidation)
		hi.setCallback(hi.conf.BUTTON_PIN_14, self._buttonValidation)
		hi.setCallback(hi.conf.BUTTON_PIN_15, self._buttonValidation)
		hi.setCallback(hi.conf.BUTTON_PIN_16, self._buttonValidation)
		hi.setCallback(hi.conf.BUTTON_PIN_17, self._buttonValidation)
		try :
			while True :
				sleep(60)
		except KeyboardInterrupt :
			pass
		hi.close()

	# Integration/service tests

	def testDepthPerception(self, delay = 1) :
		out = Output()
		inp = Input(lidar_forward_enabled = False, lidar_angled_enabled = False)
		rc = RoutineContainer(out)
		ds = DepthPerceptionService(inp, rc)
		try :
			while True :
				ds.Execute()
				sleep(delay)
		except KeyboardInterrupt :
			pass
		out.close()
		inp.close()

	def testDistanceService(self, delay = 1) :
		out = Output()
		inp = Input(lidar_angled_enabled = False, camera_enabled = False)
		rc = RoutineContainer(out)
		ds = DistanceService(inp, rc)
		try :
			while True :
				ds.Execute()
				sleep(delay)
		except KeyboardInterrupt :
			pass
		out.close()
		inp.close()

	def testTemperature(self) :
		result = subprocess.run(["vcgencmd", "measure_temp"])
