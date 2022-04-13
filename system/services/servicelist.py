# Primary Author:	<FirstName LastName (email)>
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		servicelist.py
# Description:		List of all available services (used in classmap)

# Import service code
# from system.services.templateservice import *
from system.services.depth_perception_service import *
from system.services.curb_detection_service import *
from system.services.distanceservice import *

# JSON connect name to service
servicelist = \
{
#	"TemplateService" : TemplateService
	"DepthPerceptionService" : DepthPerceptionService,
	"CurbDetectionService" : CurbDetectionService,
	"DistanceService" : DistanceService
}
