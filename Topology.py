from mininet.topo import Topo



#This class implement the topology of network, with the links and hosts names

#####
#Necessario implementar as switchs!!!
#####
class Topologia(Topo):
	def build(self,nodes,switchs,routers,edges):
		
		for node in nodes:
			host = self.addHost(node.label, cpu=.5 / len(nodes),ip=node.ip,defaultRoute=None)
		
		for switch in switchs:
			self.addSwitch(switch.label)
		
		for edge in edges:										
			if("sw" in edge.h1 and "sw" in edge.h2 ):
				self.addLink(edge.h1,edge.h2,bw = edge.bw,delay=edge.latency,loss = edge.loss)
			else:
				self.addLink(edge.h1,edge.h2, bw = edge.bw,delay=edge.latency,loss = edge.loss,
					intfName1 =edge.intfName1 ,intfName2=edge.intfName2)
			
			
	
	#This function, run for every node and configure the traffic of each host
	#receive with parameter the configuration of nodes

