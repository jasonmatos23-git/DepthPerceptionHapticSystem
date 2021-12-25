# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		DPHS.py
# Description:		Contains the main function.

import sys
from system.system import System
from system.scheduler import Scheduler
from system.hardware_interrupt import HardwareInterrupt

def main() -> int:
	DPHS: System = System()
	scheduler: Scheduler = Scheduler(DPHS.serviceContainer)
	hinterrupt: HardwareInterrupt = HardwareInterrupt(DPHS.routineContainer)
	return 0

if __name__ == "__main__" :
	sys.exit(main())
