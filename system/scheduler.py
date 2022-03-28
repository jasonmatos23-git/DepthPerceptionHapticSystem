# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		scheduler.py
# Description:		Puts services on some schedule. Modes are define here except for LPM.

from system.service_container import ServiceContainer
from system.models.service import Service
from system.mode import State, DPHSMode

from time import sleep

class Scheduler :

	def __init__(self, serviceContainer: ServiceContainer, state: State) :
		self.state: State = state
		self._prevMode: DPHSMode = self.state.getMode()
		self._depthService: Service = serviceContainer.GetService("DepthPerceptionService")
		self._general: Service = serviceContainer.GetService("GeneralMode")
		self._outdoor: Service = serviceContainer.GetService("OutdoorMode")
		self._lowpower: Service = serviceContainer.GetService("LowPowerMode")

	def GeneralMode(self) :
		self._depthService.Execute()
		sleep(0.3)	# Sleep unnecessary, used for demonstrations

	def OutdoorMode(self) :
		pass	# Curb detection + general mode

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
			if currentMode != self._prevMode :
				# Disable logic
				if self._prevMode == DPHSMode.LOW_POWER :
					self._lowpower.Execute(False)
				# Enable logic
				if currentMode == DPHSMode.LOW_POWER :
					self._lowpower.Execute(True)
				elif currentMode == DPHSMode.GENERAL :
					self._general.Execute(True)
				elif currentMode == DPHSMode.OUTDOOR :
					self._outdoor.Execute(True)
				# Set prev to new mode
				self._prevMode = currentMode
			# Run modes
			elif currentMode == DPHSMode.LOW_POWER :
				continue	# TODO: Remove this busy wait during LPM.
			elif currentMode == DPHSMode.GENERAL :
				self.GeneralMode()
			elif currentMode == DPHSMode.OUTDOOR :
				self.OutdoorMode()

