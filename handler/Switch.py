# -*- coding: utf-8 -*-
from Sniffer import Sniffer


class Switch(Sniffer):
	def __init__(self, params):
		self.label = params['name']

		self.transport_protocol = params['transport_protocol']

		self.queue = params['queue']
		self.sniffer = params['sniffer']
		self.ip = params['ip']
		self.ftp = params['ftp_server']
		# self.mask = params['mask']

		self.commands = {}

	def configComand(self,params):
		try:
			self.commands.append(params)
		except:
			lst = []
			self.commands = lst
			self.commands.append(params)
