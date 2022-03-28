# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		routinelist.py
# Description:		List of all available routines (used in classmap)

# Import service code
# from system.routines.templateroutine import *
from system.routines.depth_perception_routine import *
from system.routines.generalmode import *
from system.routines.outdoormode import *
from system.routines.lowpowermode import *
from system.routines.button_response import *

# JSON connect name to routine
routinelist = \
{
#	"TemplateRoutine" : TemplateRoutine
	"DepthPerceptionRoutine" : DepthPerceptionRoutine,
	"GeneralMode" : GeneralMode,
	"OutdoorMode" : OutdoorMode,
	"LowPowerMode" : LowPowerMode,
	"ButtonResponse" : ButtonResponse
}
