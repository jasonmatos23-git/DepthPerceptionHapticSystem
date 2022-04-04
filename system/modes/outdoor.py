# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		outdoor.py
# Description:		Define outdoor mode.

from threading import Event
from system.models.mode import Mode
from system.models.service import Service
from system.service_container import ServiceContainer
from system.modes.general import GeneralMode
from time import sleep

class OutdoorMode(Mode) :

	def __init__(self, modeChangedEvent: Event, serviceContainer: ServiceContainer, generalMode: GeneralMode) :
		self._modeChangedEvent: Event = modeChangedEvent
		self._generalMode: GeneralMode = generalMode
		# TODO: Pass in curb detection

	def enter(self) -> None:
		pass

	def exit(self) -> None:
		pass

	def Execute(self) -> None:
		while not self._modeChangedEvent.is_set() :
			self._generalMode.Execute()
			# TODO: Execute curb detection service
