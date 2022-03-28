# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		lowpowermode.py
# Description:		Play enabled/disabled indicator for low-power mode.

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

class LowPowerMode(Routine) :

	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	def _EnableMode(self) -> None:
		pass

	def _disableMode(self) -> None:
		pass

	def Execute(self, enabled: bool) -> None:
		# SPECIAL CASE MODE.
		# This script should alter outputs/system to
		# their low power modes.
		if enabled :
			self._EnableMode()
		else :
			self._disableMode()
