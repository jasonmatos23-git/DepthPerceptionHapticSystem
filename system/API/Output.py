# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

from numpy import zeros, ndarray
from enum import Enum, auto
from smbus2 import SMBus
from system.API.modules.PWM import PWM, Motor
from system.API.modules.speaker import Speaker, AUDIO

class Output :

	def __init__(self, bus: SMBus) :
		self._pwm: PWM = PWM(bus)
		self._speaker: Speaker = Speaker()	# Hard-coded to pin 12

	def __del__(self) :
		del(self._pwm)
		del(self._speaker)

	def setDutyCycle(self, location: Motor, value: int) -> None:
		# Can use this function to discretize
		self._pwm.setDutyCycle(location, value)

	def setAllDutyCycle(self,value: int) -> None:
		self._pwm.setAllDutyCycle(value)

	def setVolumeFrequency(self, volume: int, frequency: int) -> None:
		self._speaker.setVolumeFrequency(volume, frequency)

	def setVolume(self, volume: int) -> None:
		self._speaker.setVolume(volume)

	def setFrequency(self, frequency: int) -> None:
		self._speaker.setFrequency(frequency)

	def endTone(self) -> None:
		self._speaker.endTone()

	def playPattern(self, freqTimeMap: list = None, clip: AUDIO = None) -> None:
		if AUDIO is not None :
			self._speaker.playPattern(AUDIO.value)
		elif freqTimeMap is not None :
			self._speaker.playPattern(freqTimeMap)

	def setLowPower(self) -> None:
		self._pwm.setLowPower()

	def setNormalPower(self) -> None:
		self._pwm.setNormalPower()
