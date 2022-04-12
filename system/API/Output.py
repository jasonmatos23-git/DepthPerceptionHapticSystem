# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		Output.py
# Description:		Connects software components to output hardware.

from numpy import zeros, ndarray
from enum import Enum, auto
from system.API.modules.PWM import PWM, Motor
from system.API.modules.speaker import Speaker, Audio

class Output :

	def close(self) -> None:
		if self._pwm is not None :
			self._pwm.close()
			self._pwm = None
		if self._speaker is not None :
			self._speaker.close()
			self._speaker = None

	def setActive(self) -> None:
		if self._pwm is not None :
			self.setActiveMotor()
		if self._speaker is not None :
			self.setActiveSpeaker()

	def setLowPower(self) -> None:
		if self._pwm is not None :
			self.setLowPowerMotor()
		if self._speaker is not None :
			self.setLowPowerSpeaker()

	def __init__(self, motor_enabled: bool = True, speaker_enabled: bool = True) :
		self._pwm: PWM = None
		self._speaker: Speaker = None
		if motor_enabled :
			self._pwm = PWM()
		if speaker_enabled :
			self._speaker = Speaker()

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	# PUBLIC FUNCTIONS
	# Motor control
	def setDutyCycle(self, location: Motor, value: int) -> None:
		self._pwm.setDutyCycle(location, value)

	def setAllDutyCycle(self, value: int) -> None:
		self._pwm.setAllDutyCycle(value)

	def setLowPowerMotor(self) -> None:
		self._pwm.setLowPower()

	def setActiveMotor(self) -> None:
		self._pwm.setActive()

	# Speaker control
	def setVolumeFrequency(self, volume: int, frequency: int) -> None:
		self._speaker.setVolumeFrequency(volume, frequency)

	def setVolume(self, volume: int) -> None:
		self._speaker.setVolume(volume)

	def setFrequency(self, frequency: int) -> None:
		self._speaker.setFrequency(frequency)

	def endTone(self) -> None:
		self._speaker.endTone()

	def playPattern(self, audio: Audio) -> None:
		self._speaker.playPattern(audio.value)

	def setActiveSpeaker(self) -> None:
		self._speaker.setActive()

	def setLowPowerSpeaker(self) -> None:
		self._speaker.setLowPower()
