# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		system.py
# Description:		Houses state, and routine and service containers.

from system.mode import State
from system.routine_container import RoutineContainer
from system.service_container import ServiceContainer

class System :

	def __init__(self) :
		self.state: State = State()
		self.routineContainer: RoutineContainer = RoutineContainer(self.state)
		self.serviceContainer: ServiceContainer = ServiceContainer(self.routineContainer)
