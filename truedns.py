#!/usr/bin/python

import ConfigParser
import socket
import struct


def getconffile(filename):

    config = ConfigParser.ConfigParser()
    config.read(filename)

    print config.get('dnsserver','DNS1')



def rundns():

    dnss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dnss.bind(('',53))
    while 1:
        data, addr = dnss.recvfrom(1024)
        print "data %s, addr %s" % (data,addr)
#        ID = data[0:2]
#        Flags = data[2:4]

#        print struct.unpack('>H',ID)
#        print struct.unpack('>H',Flags)
        dnsinfo(data)
    #dnss.sendto(,addr)
        tt=dnsresponse()
        print "send data %s" % tt
        dnss.sendto(tt,addr)

def dnsresponse():
    dd=""
    print ID
    COM = "\x81\x80"
    print DNSOP
    QDCOUNT = '\x00\x01'
    ANCOUNT = '\x00\x01'
    NSCOUNT = '\x00\x00'
    ARCOUNT = '\x00\x01'
    qdomain = '\xc0\x0c'
    qtype = '\x00\x01'
    qclass = '\x00\x01'
    qttl = '\x00\x00\x0e\x10'
    qlen = '\x00\x04'
    qdata = '\xda\x01\x40\x21'

    qrecode = '\x00'+'\x00\x29'+'\x02\x00'+'\x00'+'\x00'+'\x00\x00'+'\x00\x00'

    dd = ID + COM + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
    dd = dd + DNSQ + qdomain + qtype + qclass + qttl + qlen + qdata
    dd = dd+ qrecode

    print "dd data is %s" % dd
    return dd

def dnsname(data):
    domain=""
    num1 = struct.unpack('B',data[0:1])
    start = 1
    num = num1[0]
    while num :
        bb= 'B'*num
        print "start %s, num %s" % (start,num)
        print struct.unpack('c'*num,data[start:num+start])
        bb = struct.unpack('c'*num,data[start:num+start])
        for x in bb:
            domain += x
        domain += "."
        num2 = struct.unpack('B',data[start+num:num+start+1])
        start = num+start+1
        num = num2[0]
        
    QTYPE = struct.unpack('>H', data[start:start+2])
    QCLASS = struct.unpack('>H', data[start+2:start+2+2])
    print domain
    print "qtype %s, qclass %s" % (QTYPE, QCLASS)
    global DNSQ
    DNSQ = data[0:start+2+2]
    print "DNSQ %s " % DNSQ


def dnsinfo(data):
# OCTET 1,2 ID
# OCTET 3,4 QR(1 bit) + OPCODE(4 bit)+ AA(1 bit) + TC(1 bit) + RD(1 bit)+ RA(1 bit) +
# Z(3 bit) + RCODE(4 bit)
# OCTET 5,6 QDCOUNT
# OCTET 7,8 ANCOUNT
# OCTET 9,10 NSCOUNT
# OCTET 11,12 ARCOUNT
    global ID 
    global DNSOP
    DNSOP = data[4:12]
    ID = data[0:2]
    COM = data[2:4]
    QDCOUNT = data[4:6]
    ANCOUNT = data[6:8]
    NSCOUNT = data[8:10]
    ARCOUNT = data[10:12]
    

    print "ID is %s" % struct.unpack('>H',ID)
    print "COM is %s" % struct.unpack('>H',COM)
    print "QDCOUNT is %s" % struct.unpack('>H',QDCOUNT)
    print "ANCOUNT is %s" % struct.unpack('>H',ANCOUNT)
    print "NSCOUNT is %s" % struct.unpack('>H',NSCOUNT)
    print "ARCOUNT is %s" % struct.unpack('>H',ARCOUNT)
    dnsname(data[12:])


def main():
    print "main"
    getconffile("truedns.conf")
    rundns()

if __name__ == "__main__":
    main()
