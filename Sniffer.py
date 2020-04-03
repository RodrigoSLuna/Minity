import os
import sys
import subprocess
import time
import argparse
import re
from datetime import datetime



class Sniffer:

	def run_sniffer(self,directory,intf):
		now = datetime.now()
		current_time = now.strftime("%H_%M_%S")
		FNULL = open(os.devnull, 'w')
		subprocess.Popen(['tcpdump', '-i', intf, '-n', 'tcp','-w', os.path.join(directory, "{}_{}.pcap".format(intf,now))], stderr = FNULL)


	def run_bufferScript(self,send,directory,interval,intf):
		now = datetime.now()
		current_time = now.strftime("%H_%M_%S")
		print("a")
		print('python2 buffer_script.py {} {} > {}.txt &'.format(interval, intf,os.path.join(directory, intf+"_"+current_time)))
		# send.cmd('./buffer_script.sh {} {} >> {}.pcap &'.format(interval, intf,os.path.join(directory, intf+"_"+current_time)))
		send.cmd('python2 buffer_script.py {} {} > {}.txt &'.format(interval, intf,os.path.join(directory, intf+"_buffer_"+current_time)))

	def run_ssScript(self,send,directory,interval,intf,ip):
		now = datetime.now()
		current_time = now.strftime("%H_%M_%S")
		# send.cmd('./ss_script.sh {} > {}.csv &'.format(interval, os.path.join(directory, ip)))