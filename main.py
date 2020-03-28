# -*- coding: utf-8 -*-
from collections import defaultdict
from Switch import Switch
from Edge import Edge
from Network import Network
from Node import Node
from Handler import Handler
from  Topology import Topologia
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import json
import io

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
	with io.open("example.json","r",encoding='utf-8') as json_file:
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
	with io.open("params.json","r",encoding='utf-8') as json_file:
		data = json.load(json_file)
		params = None
		for d in data:
			if(d['type']=='config'):
				params = d
				continue
			for node in Nodes:
				if(node.label == d['node']):
					node.configComand( d )
	return params

#https://jon.oberheide.org/blog/2008/10/15/dpkt-tutorial-2-parsing-a-pcap-file/

def main():
	configTopo()
	config = configExperimento()


	for i in range(config['n_rodadas']):
		print("Here")
		topologia = Topologia(Nodes,Switchs,Routers,Edges)
		Net = Network(topologia)
		Net.configHosts(Nodes)
		Net.configSwitchs(Switchs)
		Net.configRouter(Routers)

		Net.net.start()
		
		gerenciador = Handler()
		gerenciador.run(Nodes,Net.net,config)
		# CLI(Net.net)


		Net.net.stop()
		sleep(config['tempo_rodada']+10)
	# #Abre a interface no terminal, assim e possivel abrir um 
	# #shell para cada node, excelente para testar ideias antes de configurar a API de testes.
	# #Otimo para realizar testes para a transmissao de Dados do FTP
	
	# CLI(Net.net)



	#Menu ao usuario? Testar conexoes ?
	#Rodar experimento?
	

	# info( "Dumping host connections\n" )
	# dumpNodeConnections(Net.net.hosts)
	# info( "Testing bandwidth between h1 and h4\n" )
	# h1, h4 = Net.net.getNodeByName('h1', 'h4')
	# Net.net.iperf( ( h4, h1 ), l4Type='TCP' )
	
	# h2, h5 = Net.net.getNodeByName('h2', 'h5')
	# Net.net.iperf( ( h5, h2 ), l4Type='TCP' )
	
	# h3, h6 = Net.net.getNodeByName('h3', 'h6')
	# Net.net.iperf( ( h6, h3 ), l4Type='TCP' )
	

if __name__ == '__main__':
	main()