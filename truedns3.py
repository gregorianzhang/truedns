#/usr/bin/python
#-*- coding:utf-8 -*-

import SocketServer
import threading
import dnslib
import os
import socket,asyncore
import time
import struct

class ThreadUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        if data == 'q\n':
            os._exit(0)
        con = Controller(data)
        response1=str(con.run())
	response=data[:2]+response1[2:]
        socket = self.request[1]
        #cur_thread = threading.current_thread()
        #response = "{}: {}".format(cur_thread.name, data)
        #print "response %" % response
        #print "all data %r"  % response
        socket.sendto(response ,self.client_address)


class ThreadUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class DnsCache(object):

    global cache
    cache={}
    def __init__(self):
	pass

    def set(self,qname,qtype,qdata):
        cache[qname+"_"+qtype]=qdata

    def get(self,qname,qtype):
        return cache[qname+"_"+qtype]

    def check(self,qname,qtype):
        try:
            #print "qname %s and qtype %s" % (qname,qtype)
            cache[qname+"_"+qtype]
            return 1
        except KeyError:
            return 0

class DnsMessage(object):
    def __init__(self,data):
        self.dnsmes = dnslib.DNSRecord.parse(data)

    def getdomain(self):
        return str(self.dnsmes.q.qname)

    def gettype(self):
        return str(self.dnsmes.q.qtype)

    def getclass(self):
        return self.dnsmes.q.qclass

    def getid(self):
        return self.dnsmes.header.id

class SearchDns(object):
    def __init__(self,data):
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server=('223.6.6.6',53)
        self.server1=(('8.8.8.8',53),('208.67.220.220',53))
        self.server2=(('8.8.4.4',53),('208.67.222.222',443))
        self.socket.settimeout(5)
        self.data = data
        self.black = []
        self.dd = []
        self.hijacking = 0
        #print "self.data %r" % self.data
        self.socket.sendto(self.data,self.server)

    def run(self):
        #print "query data %r" % self.data
        qdata1=""
        while not qdata1:
            try:
                qdata1,qaddr1 = self.socket.recvfrom(2048)
                reqa = dnslib.DNSRecord.parse(qdata1)

            except:
                pass

        #print "qdata1 %r" % qdata1
        dnss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dnss.settimeout(5)
        for x in self.server1:
            #print x
            dnss.sendto(self.data,x)
            start = time.time()
            temp = []
            queue = 1
            while queue:
                end = time.time()
                if (end-start)>5:
                    queue = 0
                else:
                    try:
                        qdata2, qaddr2 = dnss.recvfrom(2048)
                        reqa = dnslib.DNSRecord.parse(qdata2)
                        #print "udp return ip address %s" % reqa.a.rdata
                        temp.append(qdata2)
                    except:
                        pass

            if len(temp) > 1:
                self.hijacking = 1
                for x in temp[:len(temp)-1]:
                    ip = dnslib.DNSRecord.parse(x)
                    blacklist.append(str(ip.a.rdata))
                break

        dnsst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dnsst.settimeout(5) 
        for x in self.server2:
            #print x
            dnsst.connect(x)
            tcpdns = struct.pack('>H',len(self.data))
            dnsst.send(tcpdns+self.data)
            qdata3 = dnsst.recv(2048)
            tcpdnsq = struct.unpack('>H',qdata3[:2])
            if tcpdnsq[0] == len(qdata3[2:]):
                reqa = dnslib.DNSRecord.parse(qdata3[2:])
                #print "tcp dns return ip address %s" % reqa.a.rdata
                if reqa.a.rdata not in blacklist:
                    break

        #print blacklist
        if self.hijacking:
            return qdata3[2:]
        else:
            return qdata1

class Controller(object):
    def __init__(self, data):
        self.data = data
        self.data1 = ''

    def run(self):
        dns=DnsMessage(self.data)
        cache1=DnsCache()
        if cache1.check(dns.getdomain(),dns.gettype()):
            self.data1 = cache1.get(dns.getdomain(),dns.gettype())
            aa = dnslib.DNSRecord.parse(self.data1)
            #print "domain %s and ip address %s" % (dns.getdomain(),aa.a.rdata)
            return self.data1
        else:
            search = SearchDns(self.data)
            bb=search.run()
            cache1.set(dns.getdomain(),dns.gettype(),bb)
            aa = dnslib.DNSRecord.parse(bb)
            #print "domain %s and ip address %s" % (dns.getdomain(),aa.a.rdata)
            return bb

if  __name__ == "__main__":
    blacklist =[]
    HOST, PORT = "0.0.0.0" , 53
    server = ThreadUDPServer((HOST,PORT),ThreadUDPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()




