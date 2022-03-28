# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		hardware_interrupt.py
# Description:		Connects routines to GPIO events.

from system.routine_container import RoutineContainer
from system.models.routine import Routine

class HardwareInterrupt :

	def __init__(self, routineContainer: RoutineContainer) :
		self.buttonResponse: Routine = routineContainer.GetRoutine("ButtonResponse")
