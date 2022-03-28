# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		scheduler.py
# Description:		Puts services on some schedule.

from system.service_container import ServiceContainer
from system.models.service import Service
from system.mode import State, DPHSMode

from time import sleep

class Scheduler :

	def __init__(self, serviceContainer: ServiceContainer, state: State) :
		self.state: State = state
		self.prevMode: DPHSMode = self.state.getMode()
		self.depthService = serviceContainer.GetService("DepthPerceptionService")

	def Run(self) :
		# Mode change indications should also be called here.
		# For general and outdoor mode, service will wrap a routine
		# which will play enalbed/disabled indicator.
		# LPM does that, and also enables/disables low power modes
		# of hardware.
		# Note: previous mode tracked to know when a mode change occurs
		# to play indicator. In LPM case, also used as a debounce for enabling
		# or disabling mode.
		while(True) :
			currentMode: DPHSMode = self.state.getMode()
			if currentMode == DPHSMode.LOW_POWER :
				continue	# Toggle LPM
			elif currentMode == DPHSMode.GENERAL :
				self.depthService.Execute()
				sleep(0.3)	# Sleep unnecessary, used for demonstrations
				continue
			elif currentMode == DPHSMode.OUTDOOR :
				continue	# Run depth + curb

