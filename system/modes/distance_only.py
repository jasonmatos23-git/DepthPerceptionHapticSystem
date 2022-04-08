# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		distance_only.py
# Description:		Demo of using distance only.

from threading import Event
from system.models.mode import Mode
from system.models.service import Service
from system.service_container import ServiceContainer
from time import sleep

class LidarMode(Mode) :

	def __init__(self, modeChangedEvent: Event, serviceContainer: ServiceContainer) :
		self._modeChangedEvent: Event = modeChangedEvent
		self.distanceService: Service = serviceContainer.GetService("DistanceService")

	def enter(self) -> None:
		pass

	def exit(self) -> None:
		pass

	def Execute(self) -> None:
		while not self._modeChangedEvent.is_set() :
			self.distanceService.Execute()
			sleep(0.100)
