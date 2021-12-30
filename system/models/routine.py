# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		routine.py
# Description:		Template and superclass for routines

from system.models.executable import Executable
from system.mode import State
from system.API.Output import Output

class Routine(Executable) :

	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_
		self.state: State = state
