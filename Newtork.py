from mininet.topo import Topo


class Topologia(Topo):
	def __init__(self,nodes,edges):
		for node in nodes:
			host = self.addHost(node.label,
                                cpu=.5 / len(nodes))

		for edge in edges:																		 #?? use_htb?
			self.addLink(edge.e1,edge.e2 switch, bw = edge.bw,delay=edge.delay,loss = edge.loss, use_htb=True)
