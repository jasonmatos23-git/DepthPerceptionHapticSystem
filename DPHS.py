# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		DPHS.py
# Description:		Contains the main function.

import sys
from system.system import System
from system.scheduler import Scheduler
from system.hardware_interrupt import HardwareInterrupt
from smbus2 import SMBus

def main() -> int:
	with SMBus(1) as i2c_bus :
		DPHS: System = System(i2c_bus)
		scheduler: Scheduler = Scheduler(DPHS.serviceContainer, DPHS.state)
		hinterrupt: HardwareInterrupt = HardwareInterrupt(DPHS.routineContainer)
		scheduler.Run()
	return 0

if __name__ == "__main__" :
	sys.exit(main())
