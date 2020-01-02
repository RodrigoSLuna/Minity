from mininet.net import Mininet
import os
import sys
import subprocess
import time
import argparse
import re

from .utils import *

class Network:

	def __init__(self, Topo):
		self.Topo = Topo
		net = Mininet(host=CPULimitedHost, link=TCLink,autoStaticArp=True)
		net.start()



	#Função que configura os Hosts internamente e externamente.
	#Configurações de Queue, Algoritmo da Camada de Transporte
	#Configurações de banda, e perda em cada Host.


	def configHosts(self, nodes):
		for node in nodes:
			send = net.get(node.label)
			#Setar o IP do send Implementar



			#Configurar FQ
		
			#A principio utiliza default de todos os parametros
			#	
			send.cmd("tc qdisc add dev eht0 root {} limit {}".format(node.queue_protocol,node.queue_length))
			#Configurar latencia na queue
			#O atraso e configurado sempre no receiver, para simular o RTT
			send.cmd("tc qdisc add dev eht0 root netem delay {} {} {} ".format(node.queue_latency,node.queue_jitter,node.queue_variation))
			#Configurar packet loss
			#Geralmente para testar a resposta dos protocolos e importante, que seja utilizado apenas em Bridges ou em Routers
			send.cmd("tc qdisc add dev eht0 root netem loss {} ".format(node.queue_loss))

			#Configurar protocolos da camada de Transporte do Host!


			#Necessário verificar se aquele algoritmo está instalado!
			algorithms = get_algorithms()

			if(node.transport_protocol not in algorithms):
				raise ValueError('Algoritmo não implementado no SO.')

			#Configura o algoritmo de transporte
			send.cmd("sysctl net.ipv4.tcp_congestion_control={}".format(node.transport_protocol))

			
