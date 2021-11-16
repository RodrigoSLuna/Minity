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
sys.path.append('./utils')
from  .. utils import *
# from .utils import algorithms
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


	#LEITURA OBRIGATORIA
	#https://www.cs.unm.edu/~crandall/netsfall13/TCtutorial.pdf
	#https://wiki.archlinux.org/index.php/Advanced_traffic_control
	#https://www.ppgia.pucpr.br/~jamhour/Pessoal/Mestrado/TARC/QoSLinux.pdf
	#http://man7.org/linux/man-pages/man8/tc-fq_codel.8.html
	#https://www.tldp.org/HOWTO/Adv-Routing-HOWTO/lartc.qdisc.classful.html
	#https://manpages.debian.org/unstable/iproute2/tc-fq_codel.8.en.html
	#https://www.systutorials.com/docs/linux/man/8-tc-tbf/
	#http://linux-ip.net/gl/tc-filters/
	#https://serverfault.com/questions/906458/network-shaping-using-tc-netem-doesnt-seem-to-work
	#https://lartc.org/howto/lartc.qdisc.classful.html
	#https://lartc.org/howto/lartc.qdisc.filters.html


	def trafficShaping(self,mode, interface, add, **kwargs):

		if mode == 'tbf':
			# print(">>>>",kwargs['buffer'])
			command = 'tc qdisc {} dev {} root handle 1: tbf rate {} buffer {} latency {}'.format('add' if add else ' change',interface, kwargs['rate'],kwards['buffer'],kwards['latency'])


		if mode == 'netem_parent':
			if(kwargs['loss'] == ''):
				param = ''
			else:
				param = 'loss'
			command = 'tc qdisc {} dev {} parent 5:1 handle 10: netem limit {} delay {} {} {} {} {}'.format('add' if add else ' change',interface, kwargs['length'],kwargs['delay'],kwargs['jitter'],kwargs['variation'],param ,kwargs['loss'])
			# command = 'tc qdisc {} dev {} parent 5:1 handle 10: netem  delay {} {} {} {} {}'.format('add' if add else ' change',interface,kwargs['delay'],kwargs['jitter'],kwargs['variation'],param ,kwargs['loss'])
		elif mode == 'netem_root':
			
			# command = 'tc qdisc {} dev {} root netem limit {} delay {} {} {} loss {}'.format('add' if add else ' change',interface,kwargs['length'] ,kwargs['delay'],kwargs['jitter'],kwargs['variation'], param ,kwargs['loss'])
			command = 'tc qdisc {} dev {} root netem limit {} delay {} {} {} loss {}'.format('add' if add else ' change',interface,kwargs['delay'],kwargs['jitter'],kwargs['variation'], param ,kwargs['loss'])
			# print(command)
		return command

	def callSniffer(self,obj,cmd):
		path = 'Framework/results/'+obj.label
		if(obj.sniffer['traffic']['status']):			
			obj.run_sniffer(path,obj.sniffer['traffic']['intf'])
			
		
		if(obj.sniffer['queue']['status']):
			obj.run_bufferScript(cmd,path,obj.sniffer['queue']['delta_t'],obj.sniffer['queue']['intf'],obj.ip)
		
		if(obj.sniffer['socket']['status']):
			obj.run_ssScript(cmd,path,obj.sniffer['socket']['delta_t'],obj.ip)


	def configHosts(self, nodes):
	
		for node in nodes:

			send = self.net.get(node.label)
			
			#A configuracao do trafego sera realizada sempre no receptor
			for edge in node.edges:
				# send.cmd("ip link set dev {} txqueuelen 1".format(edge.intfName1))
				# send2 = self.net.get(edge.h2)
				# send2.cmd("ip link set dev {} txqueuelen 1".format(edge.intfName2))
				#Configurando parametros de rede					
				if(edge.h1 == node.label):
					# print("Queue length: ", node.queue['length'],node.queue['latency'])
					send.cmd( self.trafficShaping('netem_parent',interface= edge.intfName1,add=True,delay=node.queue['latency'],jitter =node.queue['jitter'], variation= node.queue['variation'],loss =node.queue['loss'],length=node.queue['length']) )			
					
				elif(edge.h2 == node.label):
					# print("Queue length: ", node.queue['length'],node.queue['latency'])
					send.cmd( self.trafficShaping('netem_parent',interface= edge.intfName2,add=True,delay=node.queue['latency'],jitter =node.queue['jitter'], variation= node.queue['variation'],loss =node.queue['loss'],length=node.queue['length']) )			

			
			#Cria a pasta que tera os arquivos de transferencia
			send.cmd("mkdir -m 777 Framework/results/{}".format(node.label))

			# #Setar o IP do send Implementar
			# send.setIP(node.ip,node.mask)
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

			# ####Configura sniffer
			# self.callSniffer(node,send)
			
	def configSwitches(self,switchs):
		for switch in switchs:
			send = self.net.get(switch.label)
			# if(switch.label =='sw2'):
			# send.cmd("ip link set dev {} txqueuelen 1".format(switch)) #Não fez diferença no enfileiramento dos pacotes!
			#Pasta que tera os resultados
			send.cmd("mkdir -m 777 Framework/results/{}".format(switch.label))
			
			#Não se pode setar o IP para um switch.
			# send.setIP(switch.ip,switch.mask)
			# ####Configura sniffer
			# self.callSniffer(switch,send)

	def configRouter(self,routers):
		for router in routers:
			send = self.net.get(router.label)
			send.setIP(router.ip,router.mask)
			send.cmd("mkdir -m 777 Framework/results/{}".format(router.label))

			# ####Configura sniffer
			# self.callSniffer(router,send)


