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
		current_time = str(now.year) +"_" +str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_" +str(now.minute)
		FNULL = open(os.devnull, 'w')
		
		subprocess.Popen(['tcpdump', '-i', intf, '-n', 'tcp','-w', os.path.join(directory, "{}_{}.pcap".format(intf,current_time))], stderr = FNULL)
		

	def run_bufferScript(self,send,directory,interval,intf,ip):
		now = datetime.now()

		current_time = str(now.year) +"_" +str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_" +str(now.minute)

		send.cmd('python2 Framework/classes/buffer_script.py {} {} {} > {}.txt &'.format(interval, intf,ip,os.path.join(directory, intf+"_bufferQueue_{}".format(current_time))))

	def run_ssScript(self,send,directory,interval,ip):
		now = datetime.now()
		current_time = str(now.year) +"_" +str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_" +str(now.minute)
		send.cmd('python2 Framework/classes/ss_script.py {} {} > {}.txt &'.format(interval,ip,os.path.join(directory, "_bbrValues_{}".format(current_time))))