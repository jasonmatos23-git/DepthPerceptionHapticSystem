# Primary Author:	Christa Lawrence(cal47day@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		curb_detection_service.py
# Description:		

from turtle import pos
from system.models.service import Service
from system.models.routine import Routine
from system.API.Input import Input
from system.routine_container import RoutineContainer
from time import sleep


class CurbDetectionService :

	heightQueue = []	

	#startDistance: float = self.input_.GetAngledLidar() *  0.03281
	#startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281
	def __init__(self, input_: Input = None, routineContainer: RoutineContainer = None) -> None:
		self.input_: Input = input_
		self.routine:Routine = None
		if routineContainer is None:
			return
		self.curbroutine: Routine = routineContainer.GetRoutine("CurbDetectionRoutine")

		
		startHeight : float = (self.input_.GetAngledLidar() * 0.5) * 0.03281
		self.heightQueue.append(startHeight)
		#prev: float = startHeight
		
	def Execute(self) -> None:
	
		measure: float = (self.input_.GetAngledLidar() * 0.5) * 0.03281

		#remembering the last height
		self.heightQueue.append(measure) 

		while len(self.heightQueue)>5: 
			self.heightQueue.pop(0)



		qMax=max(self.heightQueue)
		qMin= min(self.heightQueue)
		qMaxIndex= self.heightQueue.index(qMax)
		qMinIndex= self.heightQueue.index(qMin)
		posiDiff: int = qMaxIndex-qMinIndex
		dif: float= float(qMax-qMin)

		#dif: float = measure-prev
		for next in self.heightQueue:
			if posiDiff == 0:
				break
			elif posiDiff > 0:
				#count diff between next and prev if its between 6 and 12 inches  
				if (dif >= 0.3) and (dif <= 1.0):
					self.curbroutine.UpExecute()
					break
				else: 
					break
			elif posiDiff < 0: 
				if (dif >= 0.3) and (dif <= 1.0):
					self.curbroutine.DownExecute()
					break
				else:
					break
			
		
