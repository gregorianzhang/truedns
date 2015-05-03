import logging
import struct

class dnsmessage(object):
    def __init__(self,data):
	self.data = data
	print data

# OCTET 1,2 ID
# OCTET 3,4 QR(1 bit) + OPCODE(4 bit)+ AA(1 bit) + TC(1 bit) + RD(1 bit)+ RA(1 bit) +
# Z(3 bit) + RCODE(4 bit)
# OCTET 5,6 QDCOUNT
# OCTET 7,8 ANCOUNT
# OCTET 9,10 NSCOUNT
# OCTET 11,12 ARCOUNT

    def dnsheader(self,data):
	logging.debug('get dnsheader %r' % data)
	ID = data[0:2]
	COM = data[2:4]
	QDCOUNT = data[4:6]
	ANCOUNT = data[6:8]
	NSCOUNT = data[8:10]
	ARCOUNT = data[10:12]



    def dnsname(self,data):
	domain1 = ""
	start = 13
	num1 = struct.unpack('B', data[12:13])
	num = num1[0]
	while num:
	    print "num %s start %s" % (num,start)
	    bb = struct.unpack('c'*num,data[start:start+num])
	    print "start %s ,num %s ,data %r " % (start,num,data[start:start+num])
	    print "bb %s" % str(bb)
	    for x in bb:
		domain1 += x
	    domain1 += "."
	    num1 = struct.unpack('B',data[start+num:start+num+1])[0]
	    start = start + num + 1
	    num = num1

	print domain1
	domain = domain1[:len(domain1)-1]
	print "len %s and start len %s " % (len(domain1),start+len(domain1))
	#domaintype = struct.unpack('BB',data[start+len(domain1):start+len(domain1)+2])
	print "data %r" % data[start+len(domain1):start+len(domain1)+2]
	#print struct.unpack('>H',data[start+len(domain1):start+len(domain1)+2])
	print "start %s" % start
	#logging.debug('get dnsname %s type %r' % (domain,domaintype))


