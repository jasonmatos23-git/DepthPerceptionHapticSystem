# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		speaker.py
# Description:		Provides functions for speaker output hardware pwm.

import pigpio
from time import sleep

class Speaker :

	def __init__(self) :
		self._pi: pigpio.pi = pigpio.pi()
		self._frequency: int = 0	# Range of 0 ~ 1,000+ Hz
		self._volume: int = 0		# Range of 0 ~ 1,000,000 (250,000 is loud)
		self._pin: int = 12			# PWM0 of pin 12

	def _updatePWM(self) -> None:
		self._pi.hardware_PWM(self._pin, self._frequency, self._volume)

	def setVolumeFrequency(self, volume: int, frequency: int) -> None:
		self._volume = volume
		self._frequency = frequency
		self._updatePWM()

	def setVolume(self, volume: int) -> None:
		self.setVolumeFrequency(volume, self._frequency)

	def setFrequency(self, frequency: int) -> None:
		self.setVolumeFrequency(self._volume, frequency)

	def endTone(self) -> None:
		self.setVolumeFrequency(0, 0)

	def playPattern(self, freqTimeMap: list) -> None:
		for tup in freqTimeMap :
			self.setFrequency(tup[0])
			sleep(tup[1])
		self.endTone()

	def close(self) -> None :
		if self._pi is None :
			return
		self._pi.stop()
		self._pi = None
