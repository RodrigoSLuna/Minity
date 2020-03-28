import argparse
import dpkt
import socket
import os
import sys
from os import listdir
from os.path import isfile, join
	


X = []
Y = []
def sending_rate(path,pcap_file,delta_t):
	import matplotlib.pyplot as plt
	file_name = os.path.join(path, pcap_file)


	f = open(file_name,'rb')

	pcap = dpkt.pcap.Reader(f)

	#ts: timestamp
	#buf: packet data length

	t = 0
	start_t = -1
	pkts = pcap.readpkts()
	total_sending_rate = []

	#Total do LINK
	#Para cada tupla e necessario 1 unico caso.


	#Dict to map all connections: (tcp_tuple, list_data_connection)
	connections = {}
	qtd_2 = 0
	for i in range(len(pkts)):
		qtd_2 += 1
		try:
			if(start_t == -1):
				start_t = pkts[i][0]
			
			eth = dpkt.ethernet.Ethernet( pkts[i][1] )	
						
			ip = eth.data	
			tcp = ip.data

			src_ip = socket.inet_ntoa(ip.src)
			dst_ip = socket.inet_ntoa(ip.dst)
			
			src_port = tcp.sport
			dst_port = tcp.dport

			tcp_tuple = (src_ip,src_port,dst_ip,dst_port)
			
			#Solucao temporaria pra evitar pegar dados da porta ftp de controle de dados
			#Talvez seja necessario para pegar quantidade de retransminssoes
			#Mas imagino que nao seja, devido a vontade de querer saber apenas a quantidade massiva de dados
			#que esteja transportando
			if(src_ip > dst_ip or dst_port == 2121 or src_port == 2121):
				continue

			try:
				data_list = connections[tcp_tuple]
				data_list.append( (pkts[i][0], pkts[i][1] ) )
				connections[tcp_tuple] = data_list

			except:
				data_list = []
				data_list.append( (pkts[i][0], pkts[i][1] ) )
				
				connections[tcp_tuple] = data_list			
		

			# total_sending_rate.append(sum_i)
		except Exception as e:
			print(e)
			print("ERRO NO PACOTE: ",i)
		
	maxi = 0
	#Faltou o tempo de cada pacote.
	connections_sending_rate = {}
	times = []
	times_not_used = []
	for key in connections:
		# print(key)
		data = connections[key]
		t = -1
		
		for i in range(len(data)):

			if(t == -1):
				t = data[i][0]

			if(data[i][0] <= t+delta_t):
				times_not_used.append(data[i][0]-start_t)
				continue

			t = data[i][0]
			time = []
			time.append(t-start_t)

			eth = dpkt.ethernet.Ethernet( data[i][1] )	

			ip = eth.data	
			
			tcp = ip.data
			maxi = max(maxi,len(tcp.data))
			
			sum_i = len(tcp.data)*8.0

			while(i+1 < len(data) and data[i+1][0] <= t+delta_t):
				time.append(data[i+1][0]-start_t)
				eth_i = dpkt.ethernet.Ethernet( data[i+1][1] )
				ip_i = eth_i.data	
				tcp_i = ip_i.data
				sum_i += len(tcp_i.data)*8.0
				maxi = max(maxi,len(tcp_i.data))
				i+=1
			times.append(time)
			# print(i,t + delta_t- start_t,sum_i)
			#Faltou agregar o tempo necessario para todos
			try:
				sums = connections_sending_rate[key]
				sums.append( ( t+delta_t- start_t ,sum_i/(delta_t*1000000) ) )
			except:
				sums = []
				sums.append( ( t+delta_t- start_t ,sum_i/(delta_t*1000000)))
				connections_sending_rate[key] = sums
			
			t = t+delta_t
	f.close()
	

	# for time in times:
	# 	print(len(time),time)
	# print("NOT USED", times_not_used)


	#Melhorar o plot.
	
	
	
	rtts = [200,10,10]
	val = 0

	for key in connections_sending_rate:
		
		x_val = [ x[0] for x in  connections_sending_rate[key]]
		y_val = [ x[1] for x in  connections_sending_rate[key]]
		X.append( (x_val,rtts[val]) )
		Y.append( (y_val,rtts[val]) )
		plt.plot(x_val,y_val,label='{} ms'.format(rtts[val]))
		val += 1
	

	# Creating zoom in and z

	plt.plot([0,50],[5,5],label = "Fair Share",ls = '--',color='red')
	plt.xlim(0,60)
	plt.title("Dois Fluxos TCP BBR")
	plt.yticks([2.5,5,7.5,10])
	plt.ylabel("Taxa de Envio [Mbit/s]")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.show()
	plt.savefig("sending_rate{}.jpg".format(path))

	plt.cla()

	
def main():
	
	mypath = "/home/rodrigoluna/Área de Trabalho/UFRJ/TCC/Framework/sw1"
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	print(onlyfiles)
	for file in onlyfiles:
		sending_rate("sw1",file,0.17355421)

	# print(X)
	# print(Y)

	#O calculo do troughtput tem que ser diferente do calculo do sending rate.
	#no Sending rate, nao possui nenhum gargalo, entao eh possivel, utilizar o tempo de marcacao do pacote
	#como o tempo que chegou naquela interface
	#No entanto, para o troughtput nao eh possivel utilizar essa abordagem, devido ao fato do pacote nao chegar
	#no mesmo tempo.
	#Nao ha mudanca no tempo do pacote, quando ele passa pelo gargalo.


	#Resolver esse problema !


	# sending_rate("sw3","sw3-eth1.pcap",0.2)



	#OUTRO PROBLEMA
	#As interfaces estão erradas, a captura deve ser feita apenas na interface sw3-eth1, assim ele não está repassando
	#os dados da propria interface



#https://github.com/jbmouret/matplotlib_for_papers?fbclid=IwAR3l0Tm4Iu_qZ5qmAxM9-eZdQtHhtAEQhm9eC0KLNMLnNzAgpRaEKnE7-aE
#https://github.com/matplotlib/AnatomyOfMatplotlib?fbclid=IwAR3epqAM73TKDGIoZAOTQYYZZPPzZz643FUORtddZRgvEfd0cgSDK9aZjko

if __name__ == '__main__':
	main()