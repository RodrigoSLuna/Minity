import subprocess
import time
import sys
from subprocess import Popen, PIPE




def get_algorithms():
	p = subprocess.check_output(['sysctl net.ipv4.tcp_available_congestion_control'],shell=True)
	return p.rstrip().split("=")[1][1:].split(" ")