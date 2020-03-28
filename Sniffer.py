import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime



class Sniffer:

	def run_sniffer(self,directory,intf):
		FNULL = open(os.devnull, 'w')
		# print("tcpdump -i {} -n tcp  -w {}".format(intf,os.path.join(directory, "{}.pcap".format(intf))))

		now = datetime.now()

		current_time = now.strftime("%H_%M_%S")
		subprocess.Popen(['tcpdump', '-i', intf, '-n', 'tcp','-w', os.path.join(directory, "{}_{}.pcap".format(intf,now))], stderr = FNULL)


