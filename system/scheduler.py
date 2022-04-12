# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		scheduler.py
# Description:		Puts services on some schedule.

from system.models.service import Service
from system.mode import State, DPHSMode
from system.models.mode import Mode
from system.system import System
from system.modes.general import GeneralMode
from system.modes.lowpower import LowPowerMode
from system.modes.outdoor import OutdoorMode

class Scheduler :

	def __init__(self, DPHS: System) :
		self.state: State = DPHS.state
		self.generalMode: Mode = GeneralMode(self.state.modeChangedEvent, DPHS.serviceContainer)
		self.lowpowerMode: Mode = LowPowerMode(self.state.modeChangedEvent, \
			DPHS.serviceContainer.input_, DPHS.routineContainer.output_)

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
			elif currentMode == DPHSMode.EXIT :
				self.state.modeChangedEvent.clear()
				break
			self.state.modeChangedEvent.clear()
