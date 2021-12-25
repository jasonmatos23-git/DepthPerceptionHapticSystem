# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		mode.py
# Description:		Mode enumeration and state getter/setter.

from enum import Enum, auto	# Provides automatic enum for system mode

class DPHSMode(Enum) :
	GENERAL = auto()
	OUTDOOR = auto()
	LOW_POWER = auto()

class State :

	def __init__(self) :
		self.state: DPHSMode = DPHSMode.GENERAL

	def getMode() -> DPHSMode :
		return self.state

	def setMode(mode: DPHSMode) -> None :
		self.state = mode
