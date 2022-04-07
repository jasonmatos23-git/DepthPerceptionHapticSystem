# Primary Author:	Christa Lawrence(cal47day@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		curb_detection_service.py
# Description:		

from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer
from time import sleep

class CurbDetectionService :

	

	#startDistance: float = self.input_.GetAngledLidar() *  0.03281
	#startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281
	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.input_: Input = input_
		self.curbroutine: Routine = routineContainer.GetRoutine("CurbDetectionRoutine")

		startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281

	
		#self.emergencyRoutine: Routine = routineContainer.GetRoutine("EmergencyResponse")
		#self.linDistRoutine: Routine = routineContainer.GetRoutine("LinearDistanceRoutine")
			

	def Execute(self) -> None:
		#measure : float = self.input_.GetAngledLidar() *  0.03281
		measure: float = (self.input_.GetAngledLidar() * 0.5) * 0.03281

		
		tmp: float = (self.startHeight-measure)

		while (abs(tmp)>=0.5):
		#if(abs(tmp)>=6.0):
			#step up
			if tmp >= 0:
				self.curbroutine.UpExecute()
			else:
				self.curbroutine.DownExecute()

		# Write image for demo
		# cv2.imwrite("input.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
		# Run model
		#measure_out: int = self._depthModel.RunInference(img)
		# Write output for demonstration
		# cv2.imwrite("output.png", img_out)
		# Call routine
		#self.routine.Execute(img_out)
