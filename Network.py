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


	#No momento estamos utilizando TBF apenas, como disciplina de filas
	#Sera necessario um modulo melhor para o gerenciamento de trafego.
	#Taxa acordada maxima < 
	#Latencia do TBF, é a latencia maxima de 1 pacote antes dele ser descartado !
	#E o quanto tempo 1 pacote pode ficar no bucket.

	#O RTT é adicionado pelo NETEM, que simula uma WAN e cria a latencia nesse caso especifico

	def traffic_shaping(mode, interface, add, **kwargs):
	    if mode == 'tbf':
	        command = 'tc qdisc {} dev {} root handle 1: tbf rate {}'.format('add' if add else ' change',interface, kwargs['rate'])
	    elif mode == 'netem':
	        command = 'tc qdisc {} dev {} parent 1: handle 2: netem delay {} {} {} loss {}'.format('add' if add else ' change',
                                                                          interface, kwargs['delay'],kwargs['jitter'],kwargs['variation'], kwargs['loss'])
	    return command



	def configHosts(self, nodes):
	

		for node in nodes:

			send = self.net.get(node.label)
			
			#A configuracao do trafego sera realizada sempre no receptor
			for edge in node.edges:
				if(edge.h1 == node.label):
					
					#Configurando parametros de rede
					
					# send.cmd( traffic_shaping('netem',interface= edge.intfName1,add=True,delay=node.queue_latency,jitter =node.queue_jitter, variation= node.queue_variation,loss =node.queue_loss) )			
					send.cmd("tc qdisc change dev {} parent 5:1 {} limit {}".format(edge.intfName1,node.queue_protocol,node.queue_length))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem delay {} {} {} ".format(edge.intfName1,node.queue_latency,node.queue_jitter,node.queue_variation))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem loss {} ".format(edge.intfName1,node.queue_loss))
				elif(edge.h2 == node.label):
					# send.cmd( traffic_shaping('netem',interface= edge.intfName2,add=True,delay=node.queue_latency,
					# 	jitter =node.queue_jitter, variation= node.queue_variation,loss =node.queue_loss) )			
					send.cmd("tc qdisc change dev {} parent 5:1 {} limit {}".format(edge.intfName2,node.queue_protocol,node.queue_length))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem delay {} {} {} ".format(edge.intfName2,node.queue_latency,node.queue_jitter,node.queue_variation))
					
					send.cmd("tc qdisc change dev {} parent 5:1 netem loss {} ".format(edge.intfName2,node.queue_loss))
			

			#Cria a pasta que tera os arquivos de transferencia
			send.cmd("mkdir -m 777 {}".format(node.label))


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
				print("Sniffer")
				path = node.label+"/"
				node.run_sniffer(path,node.sniffer['intf'])
				# node.run_bufferScript(send,path,node.sniffer['intf'])
				# node.run_ssScript(send,path,node.sniffer['intf'],node.ip)
	
	def configSwitchs(self,switchs):
		for switch in switchs:
			send = self.net.get(switch.label)
			#Pasta que tera os resultados
			send.cmd("mkdir -m 777 {}".format(switch.label))

			####Configura sniffer
			if(switch.sniffer['sniffer']):
				path = switch.label+"/"
				print("Sniffer")
				switch.run_sniffer(path,switch.sniffer['intf'])
				switch.run_bufferScript(send,path,0.004,switch.sniffer['intf'])
				switch.run_ssScript(send,path,0.004,switch.sniffer['intf'],switch.ip)



	def configRouter(self,routers):
		for router in routers:
			send = self.net.get(router.label)

			send.cmd("mkdir -m 777 {}".format(router.label))

			####Configura sniffer
			if(router.sniffer['sniffer']):
				path = router.label+"/"
				router.run_sniffer(path,router.sniffer['intf'])



		print("router")




	#Irá iniciar o experimento, e irá disparar um gerenciador de tarefas
	#que inicializá as transferências entre os hosts.
	
