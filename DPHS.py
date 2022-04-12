# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		DPHS.py
# Description:		Contains the main function.

import sys
from system.system import System
from system.scheduler import Scheduler
from system.hardware_interrupt import HardwareInterrupt
from system.API.Input import Input
from system.API.Output import Output

def main() -> int:
	input_: Input = Input()
	output_: Output = Output()
	DPHS: System = System(input_, output_)
	scheduler: Scheduler = Scheduler(DPHS)
	hinterrupt: HardwareInterrupt = HardwareInterrupt(DPHS.routineContainer)
	scheduler.Run()
	return 0

if __name__ == "__main__" :
	sys.exit(main())
