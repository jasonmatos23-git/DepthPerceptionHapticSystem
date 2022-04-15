# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		routinelist.py
# Description:		List of all available routines (used in classmap)

# Import service code
# from system.routines.templateroutine import *
from system.routines.depth_perception_routine import *
from system.routines.curb_detection_routine import *
from system.routines.button_response import *
from system.routines.linear_distance_routine import *
from system.routines.emergency_response import *

# JSON connect name to routine
routinelist = \
{
#	"TemplateRoutine" : TemplateRoutine
	"DepthPerceptionRoutine" : DepthPerceptionRoutine,
	"CurbDetectionRoutine" : CurbDetectionRoutine,
	"ButtonResponse" : ButtonResponse,
	"LinearDistanceRoutine" : LinearDistanceRoutine,
	"EmergencyResponse" : EmergencyResponse
}

