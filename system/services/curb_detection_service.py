# Primary Author:	Christa Lawrence(cal47day@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		curb_detection_service.py
# Description:		

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer

import cv2
from system.services.depthmodel.depthmodel import DepthModel
from numpy import ndarray
from time import sleep

class CurbDetectionService :

	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self._depthModel = DepthModel((3, 3))
		self.input_: Input = input_
		self.routine: Routine = routineContainer.GetRoutine("CurbDetectionRoutine")

	def Execute(self) -> None:
		img: ndarray = self.input_.GetCameraImage() #getlidar-To do in depthmodel
		# Write image for demo
		# cv2.imwrite("input.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
		# Run model
		img_out: ndarray = self._depthModel.RunInference(img)
		# Write output for demonstration
		# cv2.imwrite("output.png", img_out)
		# Call routine
		self.routine.Execute(img_out)
