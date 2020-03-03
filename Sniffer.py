import os
import sys
import subprocess
import time
import argparse
import re



class Sniffer:

	def run_sniffer(self,directory,intf):
		print("tcpdump -i {} -n tcp -s 88 -w {}".format(intf,os.path.join(directory, "{}.pcap".format(intf))))
		subprocess.Popen(['tcpdump', '-i',intf, '-n', 'tcp', '-s', '88',
                          '-w', os.path.join(directory, "{}.pcap".format(intf))])


