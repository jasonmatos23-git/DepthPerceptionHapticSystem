# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		speaker.py
# Description:		Provides functions for speaker output hardware pwm.

import pigpio
from time import sleep
from enum import Enum
from typing import List

# C D E G notes by: https://www.letsstartcoding.com/mary-little-lamb-speaker
R = 0
C = 523
D = 587
E = 659
G = 784

class Audio(Enum) :
	TEMPLATE_TUNE = [(C, 1), (R, 0.1), \
					(D, 1), (R, 0.1), \
					(E, 1), (R, 0.1), \
					(G, 1), (R, 0.1)]
	SYSTEM_STARTUP = [(C, 0.4), (R, 0.2), \
					(C, 0.2), (G, 0.4), (R, 0.4)]
	BUTTON_DOWN = [(G, 0.2), (R, 0.2)]
	GENERAL_MODE = [(C, 0.2), (R, 0.1), \
					(D, 0.2), (R, 0.1), \
					(E, 0.2), (R, 0.1)]
	OUTDOOR_MODE = [(C, 0.2), (R, 0.1), \
					(D, 0.2), (R, 0.1), \
					(D, 0.2), (R, 0.1)]
	LOW_POWER_MODE = [(C, 0.2), (R, 0.1), \
					(D, 0.2), (R, 0.1), \
					(C, 0.2), (R, 0.1)]
	EXIT = [(E, 0.2), (R, 0.1), \
			(D, 0.2), (R, 0.1), \
			(C, 0.2), (R, 0.1)]
	SYSTEM_SHUTDOWN = [(G, 0.4), (R, 0.2), \
					(G, 0.2), (C, 0.4)]

class Speaker :

	# WARNING terminating program without ending the tone
	# will cause it to persist.
	def close(self) -> None:
		if self._pi is not None and self._pi.connected :
			self.endTone()
			self._pi.stop()
			self._pi = None

	def setActive(self) -> None:
		if self._pi is None :
			self.__init__()

	def setLowPower(self) -> None:
		self.endTone()

	def __init__(self, pin: int = 12) :
		self._pi: pigpio.pi = pigpio.pi()
		self._volume_array: List[int] = [9000, 6000, 3000]
		self._vol_index: int = 0
		self._frequency: int = 0	# Range of 0 ~ 1,000+ Hz
		self._volume: int = \
			self._volume_array[self._vol_index]	# Range of 0 ~ 1,000,000 (250,000 is loud)
		self._pin: int = pin
		self.endTone()

	def __enter__(self) -> None:
		return self

	def __del__(self) -> None:
		self.close()

	def __exit__(self, err_type, err, traceback) -> None:
		self.close()

	def _updatePWM(self) -> None:
		self._pi.hardware_PWM(self._pin, self._frequency, self._volume)

	def setVolumeFrequency(self, volume: int, frequency: int) -> None:
		self._volume = volume
		self._frequency = frequency
		self._updatePWM()

	def setVolume(self, volume: int) -> None:
		self.setVolumeFrequency(volume, self._frequency)

	def incrementVolume(self) :
		self._vol_index = (self._vol_index + 1)%len(self._volume_array)
		self.setVolume(self._volume_array[self._vol_index])

	def setFrequency(self, frequency: int) -> None:
		self.setVolumeFrequency(self._volume, frequency)

	def endTone(self) -> None:
		self.setFrequency(0)

	def playPattern(self, freqTimeMap: list) -> None:
		for tup in freqTimeMap :
			self.setFrequency(tup[0])
			sleep(tup[1])
		self.endTone()
