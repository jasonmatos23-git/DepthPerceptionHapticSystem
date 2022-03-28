# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		servicelist.py
# Description:		List of all available services (used in classmap)

# Import service code
# from system.services.templateservice import *
from system.services.depth_perception_service import *
from system.services.generalmode import *
from system.services.outdoormode import *
from system.services.lowpowermode import *

# JSON connect name to service
servicelist = \
{
#	"TemplateService" : TemplateService
	"DepthPerceptionService" : DepthPerceptionService,
	"GeneralMode" : GeneralMode,
	"OutdoorMode" : OutdoorMode,
	"LowPowerMode" : LowPowerMode
}
