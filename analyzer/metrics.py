import numpy as np
import pandas as pd



def plotSendingRate():
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

	import matplotlib.pyplot as plt

	min_time = -1
	fair_shared_x = np.array([])
	fair_shared_y = np.array([])
	y_sum = 0
	i = 0
	maxi_x = 0
	for flow in df_sr['dest'].unique().tolist():
		i+=1
		label = str(round( df_queue[df_queue['ip'] == flow]['delay'].mean()*1000,2)) + "ms"
		
		
		x_vals = df_sr[df_sr['dest']==flow].time
		y_vals = df_sr[df_sr['dest']==flow].rate
		maxi_x = max(maxi_x,max(x_vals))
		y_sum += np.mean(y_vals)
		plt.plot( x_vals,y_vals,label = label  )

	y_sum /= i

	plt.plot([0,maxi_x],[y_sum,y_sum],'--',label='Fair Shared',color='red')
		
	plt.ylabel("Taxa de Envio [Mbit/s]")
	plt.xlabel("Tempo (s)")
	plt.legend()
	plt.title("N fluxos")

	plt.show()

