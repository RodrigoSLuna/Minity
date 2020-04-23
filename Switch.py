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