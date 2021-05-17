



class Edge:
	def __init__(self, params):
		self.h1 = params['VERTICE_1']
		self.h2 = params['VERTICE_2']
		self.bw = params['bw']
		self.buffer = params['buffer']
		self.latency = params['latency']
		self.loss = params['loss']
		self.intfName1 = params['intfName1']
		self.intfName2 = params['intfName2']

