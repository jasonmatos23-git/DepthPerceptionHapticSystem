# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		generalmode.py
# Description:		Play enabled/disabled indicator for general mode.

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

class GeneralMode(Routine) :

	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_

	def _EnableMode(self) -> None:
		pass

	def _disableMode(self) -> None:
		pass

	def Execute(self, enabled: bool) -> None:
		if enabled :
			self._EnableMode()
		else :
			self._disableMode()
