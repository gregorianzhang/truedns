import logging
import socket
from lib.dns import dns

class server(object):
    def __init__(self):
	pass


    def server(self):
	logging.debug("start server")
	dnss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dnss.bind(('',5311))
	while True:
	    data, addr = dnss.recvfrom(1024)
	    logging.debug("data is %s addr %s" % (data,addr))
	    tt = dns.dnsmessage(data)
	    tt.dnsheader(data)
	    tt.dnsname(data)



