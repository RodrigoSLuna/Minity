import subprocess
import time
import sys
from subprocess import Popen, PIPE,run





def get_algorithms():
	p = run(['sysctl net.ipv4.tcp_available_congestion_control'],shell=True,stdout=PIPE, stderr=PIPE, universal_newlines=True)
	return p.stdout.rstrip().split("=")[1][1:].split(" ")

