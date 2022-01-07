# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		scheduler.py
# Description:		Puts services on some schedule.

from system.service_container import ServiceContainer
from system.models.service import Service
from system.mode import State

from time import sleep

class Scheduler :

	def __init__(self, serviceContainer: ServiceContainer, state: State) :
		self.state: State = state
		self.depthService = serviceContainer.GetService("DepthPerceptionService")

	def Run(self) :
		while(1)
			self.depthService.Execute()
			sleep(5)

