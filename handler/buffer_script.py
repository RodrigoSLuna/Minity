
import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime
from time import sleep



while(True):

	#Faco a leitura dos dados que estao contidos em netem e tbf
	# os.system("tc -s -d qdisc  show dev {} | sed -n 's/.*backlog \\([^ ]*\\).*/\\1/p';tc -s -d qdisc show dev {} | sed -n 's/.*delay *//p';date +%M:%S:%3N;".format(sys.argv[2],sys.argv[2]))
	os.system("echo {} | tr \"\n\" \" \" ; tc -s -d qdisc show dev {} | tr \"\n\" \" \"; date +%M:%S:%3N ;".format(sys.argv[3],sys.argv[2]))
	sleep(float(sys.argv[1]))