# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		templateroutine.py
# Description:		Template for routines

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output

class TemplateRoutine(Routine) :

	# Initialization of vars
	def __init__(self, output_: Output = None, state: State = None) -> None:
		self.output_: Output = output_
		self.state: State = state

	# Routine logic (e.g. changing modes or sending output to motors)
	# May take parameters from a service
	def Execute(self) -> None:
		pass
