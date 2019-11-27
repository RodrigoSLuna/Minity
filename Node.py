



class Node:
	def __init__(self, params):
		self.label = params['label']
		self.transport_protocol = params['transport_protocol']
		self.queue_protocol = params['queue_protocol']
		self.queue_length = params['queue_length']