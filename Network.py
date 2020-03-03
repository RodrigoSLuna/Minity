# -*- coding: utf-8 -*-
from mininet.net import Mininet
import os
import sys
import subprocess
import time
import argparse
import re
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from utils import *

class Network:

	def __init__(self, Topo):
		self.Topo = Topo
		self.net = Mininet(topo=Topo,host=CPULimitedHost,link=TCLink,autoStaticArp=True)
		# self.net.start()

	#Função que configura os Hosts internamente e externamente.
	#Configurações de Queue, Algoritmo da Camada de Transporte
	#Configurações de banda, e perda em cada Host.

	def configHosts(self, nodes):
	

		for node in nodes:

			send = self.net.get(node.label)
			
			for edge in node.edges:
				if(edge.h1 == node.label):
					
					#Configurando parametros de rede

					# send.cmd("tc qdisc change dev {} root tbf rate {} buffer {} latency {}".format(edge.intfName1, edge.bw, ,edge.latency))


					
					send.cmd("tc qdisc change dev {} parent 5:1 {} limit {}".format(edge.intfName1,node.queue_protocol,node.queue_length))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem delay {} {} {} ".format(edge.intfName1,node.queue_latency,node.queue_jitter,node.queue_variation))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem loss {} ".format(edge.intfName1,node.queue_loss))
				elif(edge.h2 == node.label):
					send.cmd("tc qdisc change dev {} parent 5:1 {} limit {}".format(edge.intfName2,node.queue_protocol,node.queue_length))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem delay {} {} {} ".format(edge.intfName2,node.queue_latency,node.queue_jitter,node.queue_variation))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem loss {} ".format(edge.intfName2,node.queue_loss))
			

			#Cria a pasta que tera os arquivos de transferencia
			send.cmd("mkdir {}".format(node.label))


			#Setar o IP do send Implementar
			
			#Necessário verificar se aquele algoritmo está instalado!
			algorithms = get_algorithms()
			if(node.transport_protocol not in algorithms):
				raise ValueError('Algoritmo não implementado no Sistema Operacional.')

			#Configura o algoritmo de transporte
			send.cmd("sysctl net.ipv4.tcp_congestion_control={}".format(node.transport_protocol))


			#Configurando servidores FTP, caso o host seja
			#Cada nó cria um servidor FTP.
			if(node.ftp):
				node.configServer(send,node.ip)


			####Configura sniffer
			
			if(node.sniffer['sniffer']):
				path = node.label+"/"
				node.run_sniffer(path,node.sniffer['intf'])
	
	def configSwitchs(self,switchs):
		for switch in switchs:
			send = self.net.get(switch.label)
			#Pasta que tera os resultados
			send.cmd("mkdir {}".format(switch.label))

			####Configura sniffer
			if(switch.sniffer['sniffer']):
				path = switch.label+"/"
				switch.run_sniffer(path,switch.sniffer['intf'])



	def configRouter(self,routers):
		for router in routers:
			send = self.net.get(router.label)

			send.cmd("mkdir {}".format(router.label))

			####Configura sniffer
			if(router.sniffer['sniffer']):
				path = router.label+"/"
				router.run_sniffer(path,router.sniffer['intf'])



		print("router")




	#Irá iniciar o experimento, e irá disparar um gerenciador de tarefas
	#que inicializá as transferências entre os hosts.
	
