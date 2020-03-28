


class FTP:
	def retrFile(self,send,ip,node,file):
		print("python2 Client.py {} {} {}".format(ip,node,file))
		send.cmd("python Client.py {} {} {} &".format(ip,node,file))

	def configServer(self,send,ip):
		print(("python2 Server.py {} ".format(ip)))
		send.cmd("python2 Server.py {} &".format(ip))
		print("b")