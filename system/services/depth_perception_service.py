# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depth_perception_service.py
# Description:		Apply depth perception TFLite model

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

import cv2
from system.services.depthmodel.depthmodel import DepthModel
from numpy import ndarray
from time import sleep

class DepthPerceptionService :

	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.depthModel = DepthModel()
		self.input_: Input = input_
		self.routine: Routine = routineContainer.GetRoutine("DepthPerceptionRoutine")

	def Execute(self) -> None:
		for i in range(10, 0, -1) :
			print(i)
			sleep(1)
		print("Capturing image")
		img: ndarray = self.input_.GetCameraImage()
		img_out: ndarray = self.depthModel.RunInference(img.reshape((480, 640, 3)))
		# Write output for demonstration
		cv2.imwrite("output.png", img_out)
		# Call routine
		self.routine.Execute(img_out)
