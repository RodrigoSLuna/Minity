import platform

if(int(platform.python_version()[0])>=3):
	from .analyzer import *
else:
	from .classes import *