# -*- coding: utf-8 -*-
from Sniffer import Sniffer


class Switch(Sniffer):
	def __init__(self, params):
		self.label = params['name']

		self.transport_protocol = params['transport_protocol']

		self.queue_protocol = params['queue_protocol']
		self.queue_latency = params['queue_latency']
		self.queue_length = params['queue_length']
		self.queue_jitter = params['queue_jitter']
		self.queue_variation = params['queue_variation']
		self.queue_loss = params['queue_loss']

		self.sniffer = params['sniffer']
		self.ip = params['ip']

		self.ftp = params['ftp_server']