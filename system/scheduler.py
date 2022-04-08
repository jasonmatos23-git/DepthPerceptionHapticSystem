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
from system.modes.cv_only import CVMode
from system.modes.distance_only import LidarMode

class Scheduler :

	def __init__(self, serviceContainer: ServiceContainer, state: State) :
		self.state: State = state
		self.generalMode: Mode = GeneralMode(state.modeChangedEvent, serviceContainer)
		self.lowpowerMode: Mode = LowPowerMode(state.modeChangedEvent, \
			serviceContainer.input_, serviceContainer.routineContainer.output_)
		self.cvMode: Mode = CVMode(state.modeChangedEvent, serviceContainer)
		self.lidarMode: Mode = LidarMode(state.modeChangedEvent, serviceContainer)

	# NOTE: If calling Run() after the initial call ensure that
	#		the state is changed via setMode() to a mode other than
	#		the DPHSMode.EXIT or else the scheduler will return immediately.
	def Run(self) :
		self.state.modeChangedEvent.clear()
		currentMode: DPHSMode = None
		while True :
			currentMode = self.state.getMode()
			if currentMode == DPHSMode.LOW_POWER :
				self.lowpowerMode.Execute()
			elif currentMode == DPHSMode.GENERAL :
				self.generalMode.Execute()
			elif currentMode == DPHSMode.OUTDOOR :
				pass	# Execute outdoor
			elif currentMode == DPHSMode.DEMO_DISTANCE_ONLY :
				self.lidarMode.Execute()
			elif currentMode == DPHSMode.DEMO_CV_ONLY :
				self.cvMode.Execute()
			elif currentMode == DPHSMode.EXIT :
				self.state.modeChangedEvent.clear()
				break
			self.state.modeChangedEvent.clear()

