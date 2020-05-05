import dpkt
import os
import sys
import socket
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize





def get_num(x):
    val = ''
    try:
        for ele in x:
            if(ele.isdigit() or ele == '.'):
                val += ele
            else:
                break
    except:
        val = x

    return float(val)

def rate(val):
    number = get_num(val)
    if("K" in val):
        number *= 1000
    elif("M" in val):
        number *= 1000000
    elif("G" in val):
        number *= 1000000000
    return number

def mrtt_to_secs(val):
    number = get_num(val)
    number *= 0.001
    return number
    
    
def format_bbrColumns(df):

    df['bw'] = df['bw'].apply(lambda x: rate(x) )
    df['mrtt'] = df['mrtt'].apply(lambda x: mrtt_to_secs(x) ) 

    return df.fillna(0)


def to_secs(val):
    number = None
    if(isinstance(val, str)):
        number = get_num(val)
        if("ms" in val):
            number *= 0.001
    else:
        number = val* 0.001
    return number

    
def format_columns(df):
    df['rate'] = df['rate'].apply(lambda x: rate(x) )
    df['backlog'] = df['backlog'].apply(lambda x: rate(x) )
    df['burst'] = df['burst'].apply(lambda x: rate(x) )
    
    df['delay'] = df['delay'].apply(lambda x: to_secs(x) )
    df['lat'] = df['lat'].apply(lambda x: to_secs(x) )
    
    return df.fillna(0)




def sending_rate(onlyfiles,delta_t):

    id = 1
    # onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and ".pcap" in f ]
    
    datas = []
    for file in onlyfiles:
        # f = open(path+"/"+file,'rb')
        f = open(file,'rb+')
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
                pass
                # print("ERRO NO PACOTE: ",i)

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
                
                try:
                    sums = connections_sending_rate[key]
                    sums.append( ( t+delta_t- start_t ,sum_i/(delta_t*1000000) ) )
                except:
                    sums = []
                    sums.append( ( t+delta_t- start_t ,sum_i/(delta_t*1000000)))
                    connections_sending_rate[key] = sums

                t = t+delta_t
        f.close()

        val = 0

        
        for key in connections_sending_rate:
            for x in connections_sending_rate[key]:
                data_json = {"src":key[0]}
                data_json.update({"sport":key[1]})
                data_json.update({"dst":key[2]})
                data_json.update({"dport":key[3]})
                data_json.update({'time':x[0]})
                data_json.update({'rate':x[1]})
                data_json.update({'id':id})
                datas.append(data_json)
        id = id + 1
    return pd.DataFrame(datas)


def bbrParser(onlyfiles):
    data = []
    id = 1
    # onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and "bbr" in f ]
    for file in onlyfiles:
        
        # f = open(path+"/"+file,"r")
        f = open(file,"r")
        start = -1
        for line in f:
            
            data_json = {}
            
            line = line.split(" ")
            vals = []
            var = False
            for x in line:
                if(x != '' and x != '\t'):
                    vals.append(x)
            try:    
                source = vals[10].split(':')
                dest = vals[11].split(':')
                data_json = {'src':source[0]}
                data_json.update( {'sport':source[1]})
                data_json.update( {'dst':dest[0]})
                data_json.update( {'dport':dest[1]})
                
#                 print(vals[10],vals[11])
                words = ['cwnd:','bbr:']
                for x in vals:
                    if('cwnd:' in x):
                        aux = x.split(':')
                        try:
                            data_json.update({aux[0] :aux[1]})
                        except:
                            data_json = {aux[0]:aux[1]}
                    elif("bbr:" in x ):

                        aux = x.replace('(','')

                        aux = aux.replace(')','')
                        aux = aux.split(',')

    #                     print(aux)

                        #[bw:2.9Mbps],[mrtt:40.398],pacing_gain:2.88672[cwnd_gain:2.88672]
                        bbrDict = {"mrtt":0, "pacing_gain":1,"cwnd_gain":2,"bw":3}
                        v1 = [0,0,0,0]
                        for y in aux:
                            aux2 = y.split(':')
                            if(aux2[0]=='bbr'):
                                v1[ bbrDict[aux2[1]] ] = 1   
                                try:
                                    data_json.update({aux2[1]:aux2[2]})
                                except:
                                    data_json = {aux2[1]:aux2[2]}
                            elif(aux2[0] == 'mrtt' or aux2[0] == 'pacing_gain' or aux2[0] == 'cwnd_gain' ):
                                v1[ bbrDict[aux2[0]] ] = 1     
                                try:
                                    data_json.update({aux2[0]:aux2[1]})
                                except:
                                    data_json = {aux2[0]:aux2[1]}
                        if( sum(v1) == 4 ):
                            var = True
                        else:
                            data_json.update({"mrtt":0.0,
                                                "pacing_gain":0.0,
                                                "cwnd_gain":0.0,
                                                "bw":"0.0Mbps"
                                            })

            except Exception as e:
                continue
            time = vals[-1].split(":")
            
            time_s = float(time[0])*60 + float(time[1]) + 0.001*float(time[2][:-1])
            
            if(start == -1):
                start = time_s
            data_json.update({"time":time_s - start}) 
            data_json.update({"id":id})
                
            data.append(data_json)
        id = id + 1
    df = pd.DataFrame(data)
    
    return format_bbrColumns(df)

def queueParser(onlyfiles):
    # onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and "Queue" in f ]
    id = 1
    data = []
    for file in onlyfiles:
        # f = open(path+"/"+file,"r")
        f = open(file,"r")
        start = -1
        
        for line in f:
            #Parser nos dados coletados do netem
            data_json = {}
            words_netem = ['limit','delay','loss','backlog']
            words_tbf   = ['rate','burst','lat']
            line = line.split(" ")
            var = False
            for i in range(len(line)):
                if(line[i] in words_netem or line[i] in words_tbf):
                    var = True
                    aux = {line[i]:line[i+1]}
                    try:
                        data_json.update(aux)
                    except:
                        data_json = aux
                    
            if(var):
                data_json.update({"ip":line[0]})
                time = line[-1].split(":")
                time_s = float(time[0])*60 + float(time[1]) + 0.001*float(time[2][:-1])
                if(start == -1):
                    start = time_s
                data_json.update({"time":time_s - start}) 
                data_json.update({"id":id})
                data.append(data_json)
            else:
                #Criar um data vazio, mas com o time.
                continue
        id = id + 1
#     df_aux = pd.DataFrame.from_dict(json_normalize(data_json), orient='columns')
    df = pd.DataFrame(data)
    return format_columns(df)