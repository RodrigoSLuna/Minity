# -*- coding: utf-8 -*-,
import datetime
from time import sleep
import logging
class Handler():
	def run(self,nodes,switchs,Network,configs):
		
		logging.basicConfig(filename='Framework/results/example.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		time = 0
		#Mudar essa diretiva, como testar ? Deixa rodando eternamente? Interrupção?
		#Adicionar LOG 
		

		max_time = configs['tempo_rodada']


		while(time < max_time):
			# print(time) 
			for node in nodes:
				####Configura sniffer
				send = Network.net.get(node.label)
				if(time == 1):
					Network.callSniffer(node,send)
				try:
		
					for command in node.commands:
						#tc qdisc change dev h1-s1 parent 5:1 netem delay 50ms
						if(command['time'] == time):
							if(command['type'] == 'start'):
								# print(time, node.label, "Iniciou transferencia")
								logging.info(node.label + " Iniciou transferencia")

								node.retrFile(send,command['ip'],node.label,command['filename'])
							
							elif(command['type'] == 'rtt'):
								# print(time, ("tc qdisc change dev {} parent 5:1 netem delay {}".format(command['intfName'], command['value'])))
								logging.info(node.label + " Trocou rtt {}".format(command['value']))
								send.cmd("tc qdisc change dev {} parent 5:1 netem delay {}".format(command['intfName'], command['value']))

				except Exception as e:
					print(time,e)
					logging.error(e)
			

			for switch in switchs:
				send = Network.net.get(switch.label)
				####Configura sniffer
				if(time == 1):
					Network.callSniffer(switch,send)
				try:
					for command in switch.commands:
						if(command['time'] == time):
							if(command['type'] == 'bw'):
								print(time, ("tc qdisc change dev {} handle 5: tbf rate {}Mbit burst 15000b lat 2.0ms".format(command['intfName'], command['value'])))
								logging.info(switch.label + " Trocou bw {}".format(command['value']))
								send.cmd("tc qdisc change dev {} handle 5: tbf rate {}Mbit burst 15000b lat 2.0ms".format(command['intfName'], command['value']))
				except Exception as e:
					print(time,e)
					logging.error(e)
			
			# print(time)
			sleep(1.00000000111)
			time = time + 1		

