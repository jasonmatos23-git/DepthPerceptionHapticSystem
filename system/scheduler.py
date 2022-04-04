# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		scheduler.py
# Description:		Puts services on some schedule.

from system.service_container import ServiceContainer
from system.models.service import Service
from system.mode import State, DPHSMode
from system.models.mode import Mode
from system.modes.general import GeneralMode
from system.modes.lowpower import LowPowerMode
from system.modes.outdoor import OutdoorMode

class Scheduler :

	def __init__(self, serviceContainer: ServiceContainer, state: State) :
		self.state: State = state
		self.generalMode: Mode = GeneralMode(state.modeChangedEvent, serviceContainer)

	def Run(self) :
		currentMode: DPHSMode = None
		while True :
			currentMode = self.state.getMode()
			if currentMode == DPHSMode.LOW_POWER :
				pass	# Execute LPM
			elif currentMode == DPHSMode.GENERAL :
				self.generalMode.enter()
				self.generalMode.Execute()
				self.generalMode.exit()
			elif currentMode == DPHSMode.OUTDOOR :
				pass	# Execute outdoor
			elif currentMode == DPHSMode.EXIT :
				self.state.modeChangedEvent.clear()
				break
			self.state.modeChangedEvent.clear()

