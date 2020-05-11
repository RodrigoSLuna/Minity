import dpkt
import os
import sys
import socket
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from .collectors import *
from os.path import abspath


def extract(delta_t = 0.17355421):
	f = []
	bbr_files = []
	queue_files = []
	sending_files = []
	for (dirpath, dirnames, filenames) in os.walk("Framework/results/"):
		for file in filenames:
			if("bbr" in file):
				bbr_files.append(dirpath+"/"+file)
			elif(".pcap" in file):
				sending_files.append(dirpath+"/"+file)
			elif("Queue" in file):
				queue_files.append(dirpath+"/"+file)
	
	
   		
	df = sending_rate(sending_files,delta_t)
	df.to_csv("Framework/analyzer/tables/sendingrate.csv",mode="w",index=False)

	
	df = bbrParser(bbr_files)
	df.to_csv("Framework/analyzer/tables/bbrvalues.csv",index=False)

	df = queueParser(queue_files)
	df.to_csv("Framework/analyzer/tables/queuevalues.csv",index=False)

	# for folder in f:
	# 	sending_rate("Framework/results"+folder)


