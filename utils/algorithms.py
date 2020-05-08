import subprocess
import time
import sys
from subprocess import Popen, PIPE
import pandas as pd

def get_algorithms():
	p = subprocess.check_output(['sysctl net.ipv4.tcp_available_congestion_control'],shell=True)
	return p.rstrip().split("=")[1][1:].split(" ")



def mean_df(df,PK,c,c_time,dt=0.1):
	max_t = df[c_time].max()
	t = 0
	new_df = pd.DataFrame()
	while( t <= max_t):
		for flow in df[PK].unique().tolist():
			try:
				df_aux = df[(df[ c_time ] < t+dt)&(df[c_time] >= t) & ( df[PK]== flow) ]

				mean_value = df_aux[c].mean()

				df_aux[c+"_mean"] = mean_value
				df_aux[c_time+"_mean"] = t+dt
				if(len(new_df.columns) == 0):
					new_df = df_aux
				else:
					new_df = pd.concat([new_df,df_aux],ignore_index=True)

			except Exception as e:
				pass
		t = t + dt


	new_df.fillna(0,inplace=True)
	return new_df


