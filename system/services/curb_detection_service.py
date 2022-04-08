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

	heightQueue = []	

	#startDistance: float = self.input_.GetAngledLidar() *  0.03281
	#startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281
	def __init__(self, input_: Input, routineContainer: RoutineContainer) -> None:
		self.input_: Input = input_
		self.curbroutine: Routine = routineContainer.GetRoutine("CurbDetectionRoutine")

		
		startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281
		self.heightQueue.append(startHeight)
	
		#self.emergencyRoutine: Routine = routineContainer.GetRoutine("EmergencyResponse")
		#self.linDistRoutine: Routine = routineContainer.GetRoutine("LinearDistanceRoutine")
			

	def Execute(self) -> None:
		#measure : float = self.input_.GetAngledLidar() *  0.03281
		measure: float = (self.input_.GetAngledLidar() * 0.5) * 0.03281

		#remembering the last height
		self.heightQueue.append(measure) 

		while self.heightQueue.count()>5: 
			self.heightQueue.pop()

		prev: float = 0
		for next in self.heightQueue:
			if prev != 0:
				#count diff between next and prev if its between 6 and 12 inches  
				if (abs(next - prev) >= 0.5) and (abs(next - prev) <= 1):
					if (next - prev) < 0:
						self.curbroutine.UpExecute()
					else: 
						self.curbroutine.DownExecute()
				else: #next measure too far from prev measure
					self.heightQueue.clear()   #so forget all prevs
					self.heightQueue.append(measure) #but keep current measure
					break
			prev = next
		
	#	if abs(count) < valid: #could not find 4 measurements in the same direction
	#		return #not enough data points, return but keep what's heightQueue
