import os


class FTP:
	def retrFile(self,send,ip,node,file):
		send.cmd("python Framework/handler/Client.py {} {} {} &".format(ip,node,file))

	def configServer(self,send,ip):
		send.cmd("python2 Framework/handler/Server.py {} &".format(ip))
		