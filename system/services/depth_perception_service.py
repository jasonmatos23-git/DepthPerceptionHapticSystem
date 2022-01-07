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
		self._depthModel = DepthModel((24, 24))
		self.input_: Input = input_
		self.routine: Routine = routineContainer.GetRoutine("DepthPerceptionRoutine")

	def Execute(self) -> None:
		img: ndarray = self.input_.GetCameraImage()
		# Write image for demo
		cv2.imwrite("input.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
		# Run model
		img_out: ndarray = self._depthModel.RunInference(img)
		# Write output for demonstration
		sqred = (img_out/255.0)**2
		sqred = (255 * sqred).astype("uint8")
		cv2.imwrite("output_sqred.png", sqred)
		cv2.imwrite("output.png", sqred)
		# Call routine
		self.routine.Execute(img_out)
