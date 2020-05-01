import os


class FTP:
	def retrFile(self,send,ip,node,file):
		send.cmd("python Framework/classes/Client.py {} {} {} &".format(ip,node,file))

	def configServer(self,send,ip):
		send.cmd("python2 Framework/classes/Server.py {} &".format(ip))
		