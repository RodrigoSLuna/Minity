import numpy as np
import pandas as pd
from ..utils import mean_df
from .extractor import *

def plotSendingRate():
	import matplotlib.pyplot as plt
	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_queue = pd.read_csv('Framework/analyzer/tables/queuevalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	
	df_sr = mean_df(df_sr,'dst','rate','time')
	min_time = -1
	fair_shared_x = np.array([])
	fair_shared_y = np.array([])
	y_sum = 0
	i = 0
	maxi_x = 0
	for flow in df_sr['dst'].unique().tolist():
		i+=1
		label = str(round( df_queue[df_queue['ip'] == flow]['delay'].mean()*1000,2)) + "ms"
		
		
		x_vals = df_sr[df_sr['dst']==flow].time_mean
		y_vals = df_sr[df_sr['dst']==flow].rate_mean
		maxi_x = max(maxi_x,max(x_vals))
		y_sum += np.mean(y_vals)
		plt.plot( x_vals,y_vals,label = "ip: {} rtt: {}".format(flow,label)  )

	y_sum /= i

	plt.plot([0,maxi_x],[y_sum,y_sum],'--',label='Fair Shared',color='red')
		
	plt.ylabel("Taxa de Envio [Mbit/s]")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("Sending Rate - N fluxos")

	plt.show()
	plt.savefig("Framework/results/sendingrateNflows.png")
	return plt


#Plota todos os fluxos, com o seu MRTT e RTT envolvido
def plotMrttRtt():
	import matplotlib.pyplot as plt

	try:
		df_queue = pd.read_csv('Framework/analyzer/tables/queuevalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return
	
	df_queue = mean_df(df_queue,'ip','delay','time')
	df_bbr   = mean_df(df_bbr,'dst','mrtt','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_queue_aux = df_queue[ df_queue['ip'] == flow ]

		x_bbr_vals = df_bbr_aux.time_mean
		y_bbr_vals = df_bbr_aux.mrtt_mean*1000

		x_queue_vals = df_queue_aux.time_mean
		y_queue_vals = df_queue_aux.delay_mean*1000


		plt.plot(x_queue_vals,y_queue_vals,label="rtt {}".format( flow ))
		plt.plot(x_bbr_vals,y_bbr_vals, label="mrtt {}".format( flow ) )
		

	plt.ylabel("ms")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("RTT vs MRTT - N fluxos")	
	plt.show()
	plt.savefig("Framework/results/MrttRttNflows.png")
	return plt




def singleFlowPlotMrttRtt():
	import matplotlib.pyplot as plt

	try:
		df_queue = pd.read_csv('Framework/analyzer/tables/queuevalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return
	
	df_queue = mean_df(df_queue,'ip','delay','time')
	df_bbr   = mean_df(df_bbr,'dst','mrtt','time')
	
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_queue_aux = df_queue[ df_queue['ip'] == flow ]

		x_bbr_vals = df_bbr_aux.time
		y_bbr_vals = df_bbr_aux.mrtt*1000

		x_queue_vals = df_queue_aux.time
		y_queue_vals = df_queue_aux.delay*1000


		plt.plot(x_queue_vals,y_queue_vals,label="rtt {}".format( flow ))
		plt.plot(x_bbr_vals,y_bbr_vals, label="mrtt {}".format( flow ) )
		

		plt.ylabel("(ms)")
		plt.xlabel("Tempo (s)")
		plt.legend()
		plt.title("RTT vs MRTT - 1 fluxo")	
		plt.show()
		plt.savefig("Framework/results/MrttRtt_{}.png".format(flow.replace(".","_")))
		plt.clf()
	return plt





def plotBW():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_sr = mean_df(df_sr,'dst','rate','time')
	df_bbr   = mean_df(df_bbr,'dst','bw','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 
		y_sr_vals = df_sr_aux.rate

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.bw/10**6


		plt.plot(x_sr_vals,y_sr_vals,label="BtlBW {}".format( flow ))
		plt.plot(x_bbr_vals,y_bbr_vals, label="Estimated {}".format( flow ) )


	plt.ylabel("Mbit/s ")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("BtlBW vs EstimatedBW - N fluxos")
	plt.savefig("Framework/results/BWEstimatedNFlows.png")
	plt.show()
	return plt


def plotCWND():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','cwnd','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.cwnd_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="cwnd {}".format( flow ) )


	plt.ylabel("Segments")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("Congestion Windown - N fluxos")
	plt.savefig("Framework/results/CWNDNflow.png")
	plt.show()
	return plt

def plotPG():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','pacing_gain','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.pacing_gain_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="ip {}".format( flow ) )


	plt.ylabel("Factor")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("Pacing Gain - N fluxos")
	plt.savefig("Framework/results/PacingGainNflow.png")
	plt.show()
	return plt

def singlePlotCWND():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','cwnd','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.cwnd_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="ip {}".format( flow ) )


		plt.ylabel("Segments")
		plt.xlabel("Tempo (s)")
		plt.legend()
		plt.title("Congestion Windown - 1 fluxo")
		plt.savefig("Framework/results/CWND_{}.png".format(flow.replace(".","_")))
		plt.show()
	return plt


def plotCG():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','cwnd_gain','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.cwnd_gain_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="ip {}".format( flow ) )


	plt.ylabel("Factor")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.savefig("Framework/results/CWNDGAIN.png")
	plt.title("Congestion Windown Gain - N fluxos")
	plt.show()
	return plt


def singlePlotCG():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','cwnd_gain','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.cwnd_gain_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="ip {}".format( flow ) )


		plt.ylabel("Factor")
		plt.xlabel("Tempo (s)")
		plt.legend()
		plt.title("Congestion Windown Gain - 1 fluxo")
		plt.savefig("Framework/results/CWNDGAIN_{}.png".format( flow.replace(".","_") ) )
		plt.show()
	return plt



def singlePlotPG():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_bbr   = mean_df(df_bbr,'dst','pacing_gain','time')
	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]

		x_sr_vals = df_sr_aux.time 

		x_bbr_vals = df_bbr_aux.time + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.pacing_gain_mean


		plt.plot(x_bbr_vals,y_bbr_vals, label="ip {}".format( flow ) )


		plt.ylabel("Factor")
		plt.xlabel("Tempo (s)")
		plt.legend()
		plt.savefig("Framework/results/PacingGain_{}.png".format( flow.replace(".","_") ) )
		plt.title("Pacing Gain - 1 fluxo")
		plt.show()
	return plt




def singlePlotBW():
	import matplotlib.pyplot as plt

	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	try:
		df_bbr = pd.read_csv('Framework/analyzer/tables/bbrvalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_sr = mean_df(df_sr,'dst','rate','time')
	df_bbr   = mean_df(df_bbr,'dst','bw','time')

	for flow in df_bbr['dst'].unique().tolist():
		
		df_bbr_aux = df_bbr[ df_bbr['dst'] == flow ]

		df_sr_aux = df_sr[ df_sr['dst'] == flow ]



		x_sr_vals = df_sr_aux.time_mean 
		y_sr_vals = df_sr_aux.rate_mean

		x_bbr_vals = df_bbr_aux.time_mean + x_sr_vals.iloc[0]
		y_bbr_vals = df_bbr_aux.bw_mean/10**6
		
		
		plt.plot(x_sr_vals,y_sr_vals,label="BtlBW {}".format( flow ))
		plt.plot(x_bbr_vals,y_bbr_vals, label="Estimated {}".format( flow ) )


		plt.ylabel("Mbit/s")
		plt.xlabel("Tempo (s)")
		plt.legend()
		plt.title("BtleBW vs Estimated - 1 fluxo")
		plt.show()
		plt.savefig("Framework/results/BWEstimated_{}.png".format( flow.replace(".","_") ) )
		plt.clf()
	return plt



def plotQueue():
	import matplotlib.pyplot as plt

	try:
		df_queue = pd.read_csv('Framework/analyzer/tables/queuevalues.csv')
	except Exception as e:
			print(e)
			print("File not found")
			return
	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_queue = mean_df(df_queue,'ip','backlog','time')
	for flow in df_queue['ip'].unique().tolist():
		try:
			df_queue_aux = df_queue[df_queue['ip'] == flow]
			df_sr_aux = df_sr[ df_sr['dst'] == flow ]
			x_sr_vals = df_sr_aux.time 

			x_queue_vals = df_queue_aux['time_mean'] + x_sr_vals.iloc[0]
			y_queue_vals = df_queue_aux['backlog_mean']
			
			delay = round(np.mean(df_queue_aux['delay'])*1000,2)
			
			if(delay > 0.0):
				plt.plot(x_queue_vals,y_queue_vals, label="delay {} ip {}".format(delay,flow ) )
		except:
			pass

	plt.ylabel("Bytes")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("Queue buffer - N fluxos")
	plt.savefig("Framework/results/QueueBufferNFlows.png")
	plt.show()
	return plt



def singlePlotQueue():
	import matplotlib.pyplot as plt

	try:
		df_queue = pd.read_csv('Framework/analyzer/tables/queuevalues.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return
	
	try:
		df_sr = pd.read_csv('Framework/analyzer/tables/sendingrate.csv')
	except Exception as e:
		print(e)
		print("File not found")
		return

	df_queue = mean_df(df_queue,'ip','backlog','time')
	for flow in df_queue['ip'].unique().tolist():
		print(flow)
		try:
			df_queue_aux = df_queue[df_queue['ip'] == flow]
		
			df_sr_aux = df_sr[ df_sr['dst'] == flow ]
			x_sr_vals = df_sr_aux.time 

			x_queue_vals = df_queue_aux['time_mean'] + x_sr_vals.iloc[0]
			y_queue_vals = df_queue_aux['backlog_mean']
		
			delay = round(np.mean(df_queue_aux['delay'])*1000,2)
		
			if(delay > 0.0):
				plt.plot(x_queue_vals,y_queue_vals, label="delay {}, ip {}".format(delay,flow ) )


				plt.ylabel("Bytes")
				plt.xlabel("Tempo (s)")
				plt.legend()
				plt.title("Queue Buffer - 1 Fluxo")
				plt.savefig("Framework/results/QueueBuffer_{}.png".format( flow.replace(".","_") ))
				plt.show()
				plt.clf()
		except:
			pass
	return plt


def run(cli=False,iperf=False):
	print("Extraindo informações das tabelas")
	extract()
	print("Plot singlePlotQueue")
	singlePlotQueue()
	print("Plot plotQueue")
	plotQueue()
	print("Plot plotBW")
	singlePlotBW()
	print("Plot singlePlotPG")
	singlePlotPG()
	print("Plot singlePlotCG")
	singlePlotCG()
	print("Plot plotCG")
	plotCG()
	print("Plot singlePlotCWND")
	singlePlotCWND()
	print("Plot BW")
	plotBW()
	print("Plot singlePlotMrttRtt")
	singleFlowPlotMrttRtt()
	print("Plot plotMrttRtt")
	plotMrttRtt()
	print("Plot plotSendingRate")
	plotSendingRate()