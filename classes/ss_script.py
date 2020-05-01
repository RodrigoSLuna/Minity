import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime
from time import sleep



while(True):
	os.system("ss -tin src {} sport neq :2121 | tr \"\n\" \" \"; date +%M:%S:%3N;".format(sys.argv[2]))
	sleep(float(sys.argv[1]))