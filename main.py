from Edge import Edge
from Network import Network
from Node import Node
from  Topology import Topologia
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel, info


def buildDict(_label,_transport_protocol,_queue_protocol,_queue_latency,
	_queue_length,_queue_jitter,_queue_variation,_queue_loss,_switch,_ip,_ftp):
	a = {}
	a['label'] = _label
	a['transport_protocol'] = _transport_protocol
	a['queue_protocol'] = _queue_protocol
	a['queue_latency'] = _queue_latency
	a['queue_length'] = _queue_length
	a['queue_jitter'] = _queue_jitter
	a['queue_variation'] = _queue_variation
	a['queue_loss'] = _queue_loss
	a['switch'] = _switch
	a['ip'] = _ip
	a['ftp'] = _ftp
	return a;

Nodes = []

dict_a = buildDict('h1','bbr','fq_codel','','','','','0.1',False,'10.0.0.1',False)
dict_b = buildDict('s1','bbr','fq_codel','','','','','0.1',True,'10.0.0.2',False)

Nodes.append( Node(dict_a)  )
Nodes.append(Node(dict_b))

Edges = []

edge = {}
edge['host1'] = 'h1'
edge['host2'] = 's1'
edge['bw'] = 10
edge['delay'] = '5ms'
edge['loss'] = 0

Edges.append(Edge(edge))

topologia = Topologia(Nodes,Edges)

net = Mininet( topo=topologia,host=CPULimitedHost, link=TCLink)

net.start()

info( "Dumping host connections\n" )
dumpNodeConnections(net.hosts)