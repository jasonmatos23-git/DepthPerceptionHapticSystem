# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		general.py
# Description:		Define general mode.

from threading import Event
from system.models.mode import Mode
from system.models.service import Service
from system.service_container import ServiceContainer
from time import sleep

class GeneralMode(Mode) :

	def __init__(self, modeChangedEvent: Event, serviceContainer: ServiceContainer) :
		self._modeChangedEvent: Event = modeChangedEvent
		self.depthService: Service = serviceContainer.GetService("DepthPerceptionService")

	def enter(self) -> None:
		pass

	def exit(self) -> None:
		pass

	def Execute(self) -> None:
		while not self._modeChangedEvent.is_set() :
			self.depthService.Execute()
			sleep(0.3)	# Sleep maintained for demo purposes
