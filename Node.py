



class Node:
	def __init__(self, params):
		self.label = params['label']
			
		self.switch = params['switch']

		self.transport_protocol = params['transport_protocol']

		self.queue_protocol = params['queue_protocol']
		self.queue_latency = params['queue_latency']
		self.queue_length = params['queue_length']
		self.queue_jitter = params['queue_jitter']
		self.queue_variation = params['queue_variation']
		self.queue_loss = params['queue_loss']

		#IP of hosts
		self.ip = params['ip']

		#Variable thats have FTP configurated or not.
		self.ftp = params['ftp']



