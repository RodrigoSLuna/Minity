# -*- coding: utf-8 -*-
from Ftp import FTP
from Sniffer import Sniffer



#Necessário criar a nocao de comandos a serem ajustados
#durante a transmissão.
#MultiMap(tempo, comando)
class Node(FTP,Sniffer):
	def __init__(self, params):
		self.label = params['name']

		self.transport_protocol = params['transport_protocol']

		self.queue_protocol = params['queue_protocol']
		self.queue_latency = params['queue_latency']
		self.queue_length = params['queue_length']
		self.queue_jitter = params['queue_jitter']
		self.queue_variation = params['queue_variation']
		self.queue_loss = params['queue_loss']
		self.ip = params['ip']

		self.sniffer = params['sniffer']
		self.ftp = params['ftp_server']

		self.commands = {}

	def configComand(self,params):
		try:
			self.commands.append(params)
		except:
			lst = []
			self.commands = lst
			self.commands.append(params)

	def addEdge(self, edge):

		try:
			self.edges.append(edge)
		except:
			self.edges = []
			self.edges.append(edge)