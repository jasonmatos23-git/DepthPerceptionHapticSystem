# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		button_response.py
# Description:		Alter system and output in response to hardware interrupt.

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.mode import DPHSMode

class ButtonResponse(Routine) :

	def __init__(self, output_: Output = None, state: State = None) -> None:
		self.output_: Output = output_
		self.state: State = state

	# On button press, should play an indication that a button
	# press was registered, and change the state.
	def Execute(self) -> None:
		# Respond to general button press (speaker and/or haptic output)
		print("Button press received.")

	# Callback functions
	def Button1Down(self, channel) -> None:
		self.Execute()
		self.state.setMode(DPHSMode.GENERAL)

	def Button2Down(self, channel) -> None:
		pass

	def Button3Down(self, channel) -> None:
		pass

	def Button4Down(self, channel) -> None:
		pass

	def Button5Down(self, channel) -> None:
		self.Execute()
		self.state.setMode(DPHSMode.EXIT)
