# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depth_perception_service.py
# Description:		Apply depth perception TFLite model

# Code modified from https://tfhub.dev/intel/lite-model/midas/v2_1_small/1/lite/1
# TFLite model used without modification.
# Licenced under MIT License

# from system.models.service import Service
# from system.models.routine import Routine
# from system.API.Input import Input
# from system.routine_container import RoutineContainer

from Input import Input

import cv2
from depthmodel.depthmodel import DepthModel
from numpy import ndarray
from time import sleep

class DepthPerceptionService :

	# def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
	# 	self.input_: Input = input_
	# 	self.routine: Routine = routineContainer.GetRoutine("TemplateRoutine")

	def __init__(self, input_: Input) :
		self.depthModel = DepthModel()
		self.input_: Input = input_

	def Execute(self) -> None:
		for i in range(10, 0, -1) :
			print(i)
			sleep(1)
		print("Capturing image")
		img: ndarray = self.input_.GetCameraImage()
		img_out: ndarray = self.depthModel.RunInference(img.reshape((480, 640, 3)))
		cv2.imwrite("output.png", img_out)
