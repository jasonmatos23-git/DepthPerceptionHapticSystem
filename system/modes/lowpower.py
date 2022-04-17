# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		lowpower.py
# Description:		Define low power mode.

from threading import Event
from system.service_container import ServiceContainer
from system.models.service import Service
from system.models.mode import Mode
from system.API.Input import Input
from system.API.Output import Output

class LowPowerMode(Mode) :

	def __init__(self, modeChangedEvent: Event, input_: Input, output_: Output) :
		self._modeChangedEvent: Event = modeChangedEvent
		self._input_: Input = input_
		self._output_: Output = output_

	def enter(self) -> None:
		pass

	def exit(self) -> None:
		pass

	def Execute(self) -> None:
		# Enable LPMs
		self._input_.setLowPower()
		self._output_.setLowPower()
		# Wait for mode change
		self._modeChangedEvent.wait()
		# Disable LPMs
		self._input_.setActive()
		self._output_.setActive()
