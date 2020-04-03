
import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime
from time import sleep



while(True):
	os.system("tc -s -d qdisc show dev {} | sed -n 's/.*backlog \\([^ ]*\\).*/\\1/p'".format(sys.argv[2]))
	sleep(float(sys.argv[1]))