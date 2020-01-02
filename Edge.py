



class Edge:
	def __init__(self, params):
		self.h1 = params['host1']
		self.h2 = params['host2']
		self.bw = params['bw']
		self.delay = params['delay']
		self.loss = params['loss']

