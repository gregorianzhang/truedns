import logging
import socket
from lib.dns import dns

class server(object):
    def __init__(self):
	pass


    def server(self):
	#logging.debug("start server")
	dnss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dnss.bind(('172.18.102.2',53))
        data1 = ""
	while True:
            data, addr = dnss.recvfrom(1024)
            logging.debug("data is %r addr %s" % (data,addr))
            tt = dns.dnsmessage(data)
            ee=tt.dnsname(data)
            #logging.debug("ee %r" % ee)
            
            dnss.sendto(ee,addr)


