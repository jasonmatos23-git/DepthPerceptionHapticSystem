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
from system.API.modules.speaker import Audio
from system.configure import Configuration

def main() -> int:
	# Acquire resources
	config: Configuration = Configuration()
	output_: Output = Output()
	output_.playPattern(Audio.SYSTEM_STARTUP)
	input_: Input = Input()
	DPHS: System = System(input_, output_)
	scheduler: Scheduler = Scheduler(DPHS)
	hinterrupt: HardwareInterrupt = HardwareInterrupt(DPHS.routineContainer, config)
	# Run system
	scheduler.Run()
	# Release resources
	hinterrupt.close()
	input_.close()
	output_.playPattern(Audio.SYSTEM_SHUTDOWN)
	output_.close()
	config.close()
	return 0

if __name__ == "__main__" :
	sys.exit(main())
