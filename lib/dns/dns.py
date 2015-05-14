import logging
import struct
from lib.cache import cache
import socket
#from lib.server import server

class dnsmessage(object):
    def __init__(self,data):
	self.data = data
        self.blackdns = "4.4.4.4"

# OCTET 1,2 ID
# OCTET 3,4 QR(1 bit) + OPCODE(4 bit)+ AA(1 bit) + TC(1 bit) + RD(1 bit)+ RA(1 bit) +
# Z(3 bit) + RCODE(4 bit)
# OCTET 5,6 QDCOUNT
# OCTET 7,8 ANCOUNT
# OCTET 9,10 NSCOUNT
# OCTET 11,12 ARCOUNT

    def dnsheader(self,data):
	#logging.debug('get dnsheader %r' % data)
	ID = data[0:2]
	COM = data[2:4]
	QDCOUNT = data[4:6]
	ANCOUNT = data[6:8]
	NSCOUNT = data[8:10]
	ARCOUNT = data[10:12]



    def dnsname(self,data):
        zz = cache.cachem()

        #logging.debug("dns header id %r " % data[0:2])
	ID = data[0:2]
	domain1 = ""
	start = 13
	num1 = struct.unpack('B', data[12:13])
	num = num1[0]
	while num:
            #print "num %s start %s" % (num,start)
            bb = struct.unpack('c'*num,data[start:start+num])
            #print "start %s ,num %s ,data %r " % (start,num,data[start:start+num])
            #print "bb %s" % str(bb)
            for x in bb:
		domain1 += x
            domain1 += "."
            num1 = struct.unpack('B',data[start+num:start+num+1])[0]
            start = start + num + 1
            num = num1

	#print domain1
	domain = domain1[:len(domain1)-1]
        print "domain %s" % domain
	#print "len %s and start len %s " % (len(domain1),start+len(domain1))
	domaintype = struct.unpack('!H',data[start:start+2])[0]
        #print "domaintype %s" % domaintype

	#logging.debug('get dnsname %s type %s' % (domain,domaintype))

        #print "cache check %r" % zz.check(domain,domaintype)
        if zz.check(domain,domaintype):
            #logging.debug("get cache")
            logging.debug("domain in cache %s" % domain)
            cached = zz.get(domain,domaintype)
            #print "cached %r" % cached
        else:
            #print "forword dns message"
#            yy = server.server()
#            yy.froword(data)
            logging.debug("domain %s" % domain)
            dnsserc=('223.5.5.5',53)
            dnssc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dnssc.settimeout(5.0)
            dnssc.sendto(data,dnsserc)
            #logging.debug("send dns query to %s" % dnsserc[0])
            qdata = ""
            try:
                qdata,qaddr = dnssc.recvfrom(1024)
                #logging.debug("qdata %r qaddr %s" % (qdata,qaddr))
            except socket.timeout:
                #logging.debug("send query domain1 %s is time out" % domain)
                pass

            if qdata:
                #while qaddr[0] in self.blackdns:
                #    qdata,qaddr = dnssc.recvfrom(1024)
                zz.set(domain,domaintype,qdata)
                cached = qdata
            else:
                return "error"
 
        qid= cached[0:2]
        #print "id %r qid %r" % (ID,qid)
        cachedata = ID+cached[2:]

        return cachedata










