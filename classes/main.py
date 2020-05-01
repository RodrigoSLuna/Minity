# -*- coding: utf-8 -*-
from collections import defaultdict
from Switch import Switch
from Edge import Edge
from Network import Network
from Node import Node
from Handler import Handler
from Topology import Topologia
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import json
import io

import os
from time import sleep

Nodes = []
Switchs = []
Routers = []
Edges = []



#Adicionar uma pasta para cada LABEL do experimento, armazenar os dados numa pasta em separado !

#Próximo passo:
#Adicionar coleta estatística com tcpdump.
#Verificar se está ok.

def configTopo():
	with io.open("../config/config.json","r",encoding='utf-8') as json_file:
		data = json.load(json_file)
		
		for d in data:
			if(d['type'] == "HOST"):
				Nodes.append(Node(d))
			elif(d['type'] == "SWITCH"):
				Switchs.append(Switch(d))
			elif(d['type'] == "EDGE"):
				Edges.append(Edge(d))
			else:
				Routers.append(d)	

	for node in Nodes:
		for edge in Edges:
			if(edge.h1 == node.label or edge.h2 == node.label):
				node.addEdge(edge)


def configExperimento():
	with io.open("../config/params.json","r",encoding='utf-8') as json_file:
		data = json.load(json_file)
		params = None
		for d in data:
			if(d['type']=='config'):
				params = d
				continue
			for node in Nodes:
				if(node.label == d['node']):
					node.configComand( d )
			for switch in Switchs:
				if(switch.label == d['node']):
					switch.configComand( d )
	return params



def main():
	os.system("mn -c ")

	configTopo()
	config = configExperimento()

	
	for i in range(config['n_rodadas']):
		
		topologia = Topologia(Nodes,Switchs,Routers,Edges)
		Net = Network(topologia)
		Net.configHosts(Nodes)
		Net.configSwitchs(Switchs)
		Net.configRouter(Routers)

		Net.net.start()
		
		gerenciador = Handler()
<<<<<<< HEAD:classes/main.py
		gerenciador.run(Nodes,Switchs,Net,config)
		# h1, h4 = Net.net.getNodeByName('h1', 'h4')
		# Net.net.iperf( ( h1, h4 ), l4Type='TCP' )

		# CLI(Net.net)
=======
		gerenciador.run(Nodes,Switchs,Net.net,config)
		h1, h4 = Net.net.getNodeByName('h1', 'h4')
		Net.net.iperf( ( h1, h4 ), l4Type='TCP' )

		CLI(Net.net)

>>>>>>> parent of f0d6e7a... Adicionado novas features:main.py
		Net.net.stop()

if __name__ == '__main__':
	main()