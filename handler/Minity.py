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
import sys

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

def configTopo(filename):
	#Framework/config/conf_exp_6.json
	with io.open(filename,"r",encoding='utf-8') as json_file:
		data = json.load(json_file)
		
		for d in data:
			if(d['type'] == "HOST"):
				Nodes.append(Node(d))
			elif(d['type'] == "SWITCH" or d['type'] == "ROUTER"):
				Switchs.append(Switch(d))
			elif(d['type'] == "EDGE"):
				Edges.append(Edge(d))
			else:
				Routers.append(d)	

	for node in Nodes:
		for edge in Edges:
			if(edge.h1 == node.label or edge.h2 == node.label):
				node.addEdge(edge)


def configExperimento(filename):
	#Framework/config/params_exp_6_3.json
	with io.open(filename,"r",encoding='utf-8') as json_file:
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




def startIperf(Net):
	for node_x in Nodes:
		for node_y in Nodes:
			if(node_x.label == node_y.label):
				continue
			h_x, h_y = Net.net.getNodeByName(node_x.label, node_y.label)
			Net.net.iperf( ( h_x, h_y ), l4Type='TCP' )

def run(cli=False,iperf=False,config=None,exp=None):
	os.system("mn -c ")
	configTopo("Framework/config/"+config)
	config = configExperimento("Framework/config/"+exp)


	for i in range(config['n_rodadas']):
		
		topologia = Topologia(Nodes,Switchs,Routers,Edges)
		Net = Network(topologia)
		Net.configHosts(Nodes)
		Net.configSwitches(Switchs)
		Net.configRouter(Routers)

		Net.net.start()
		

		if(iperf):
			startIperf(Net)
		elif(cli):
			CLI(Net.net)
		else:
			gerenciador = Handler()
			gerenciador.run(Nodes,Switchs,Net,config)
		
		Net.net.stop()
