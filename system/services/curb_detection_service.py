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
		prev: float = startHeight
		
	def Execute(self) -> None:
	
		measure: float = (self.input_.GetAngledLidar() * 0.5) * 0.03281

		#remembering the last height
		self.heightQueue.append(measure) 

		while len(self.heightQueue)>5: 
			self.heightQueue.pop()

		dif: float = measure-prev
		for next in self.heightQueue:
			if dif != 0:
				#count diff between next and prev if its between 6 and 12 inches  
				if (abs(dif) >= 0.5) and (abs(dif) <= 1.0):
					if (next - prev) < 0.0:
						self.curbroutine.UpExecute()
						prev = measure
						break
					else: 
						self.curbroutine.DownExecute()
						prev = measure
						break
				else: #next measure too far from prev measure
					break
			prev = measure
		
