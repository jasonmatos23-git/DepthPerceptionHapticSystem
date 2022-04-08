# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		button_response.py
# Description:		Alter system and output in response to hardware interrupt.

from system.models.routine import Routine
from system.mode import State
from system.API.Output import Output
from system.mode import DPHSMode
from system.API.modules.speaker import AUDIO

class ButtonResponse(Routine) :

	def __init__(self, output_: Output, state: State) -> None:
		self.output_: Output = output_
		self.state: State = state

	# On button press, should play an indication that a button
	# press was registered, and change the state.
	def Execute(self) -> None:
		# Respond to general button press (speaker and/or haptic output)
		print("Button press received.")
		self.output_.playPattern(AUDIO.BUTTON_PRESS)

	# Callback functions
	def Button1Down(self, channel) :
		self.Execute()
		self.state.setMode(DPHSMode.GENERAL)
		self.output_.playPattern(AUDIO.GEN_MODE)

	def Button2Down(self, channel) :
		self.Execute()
		self.state.setMode(DPHSMode.LOW_POWER)
		self.output_.playPattern(AUDIO.LOW_POWER)

	def Button3Down(self, channel) :
		self.Execute()
		self.state.setMode(DPHSMode.DEMO_DISTANCE_ONLY)
		self.output_.playPattern(AUDIO.DEMO_DISTANCE)

	def Button4Down(self, channel) :
		self.Execute()
		self.state.setMode(DPHSMode.DEMO_CV_ONLY)
		self.output_.playPattern(AUDIO.DEMO_CV)

	def Button5Down(self, channel) :
		self.Execute()
		self.state.setMode(DPHSMode.EXIT)
