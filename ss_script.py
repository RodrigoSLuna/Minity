import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime
from time import sleep



while(True):
	os.system("ss -tin | sed -n -e 's/.* cwnd:\\([0-9]*\\).* bbr:(\\([^)]*\\)).*/\\1;;\\2/p' -e 's/.* cwnd:\\([0-9]*\\).* ssthresh:\\([0-9]*\\).*/\\1;\\2;/p';")
	sleep(float(sys.argv[1]))