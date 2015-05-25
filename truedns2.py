#/usr/bin/python
#-*- coding:utf-8 -*-

import SocketServer
import threading
import dnslib
import os
import socket,asyncore


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
        self.socket.settimeout(5.0)
        self.data = data
        self.black = ('74.125.127.102', '74.125.155.102', '74.125.39.102', '74.125.39.113', '189.163.17.5', '209.85.229.138', '249.129.46.48', '128.121.126.139', '159.106.121.75', '169.132.13.103', '192.67.198.6', '202.106.1.2', '202.181.7.85', '203.161.230.171', '203.98.7.65', '207.12.88.98', '208.56.31.43', '209.145.54.50', '209.220.30.174', '209.36.73.33', '211.94.66.147', '213.169.251.35', '216.221.188.182', '216.234.179.13', '243.185.187.39', '37.61.54.158', '4.36.66.178', '46.82.174.68', '59.24.3.173', '64.33.88.161', '64.33.99.47', '64.66.163.251', '65.104.202.252', '65.160.219.113', '66.45.252.237', '72.14.205.104', '72.14.205.99', '78.16.49.15', '8.7.198.45', '93.46.8.89',)
        #print "self.data %r" % self.data
        self.socket.sendto(self.data,self.server)

    def run(self):
        qdata1=""
        while not qdata1:
            try:
                qdata1,qaddr1 = self.socket.recvfrom(1024)
                #print "search dns run qdata1" % qdata1
                reqa = dnslib.DNSRecord.parse(qdata1)
                #print "reqa ip %s" % reqa.a.rdata
                if str(reqa.a.rdata) in self.black:
                    qdata1 = ""

            except:
                pass
            #reqa = dnslib.DNSRecord.parse(qdata1)
            #print "reqa ip %s" % reqa
        #qdata,qaddr = self.socket.recvfrom(1024)
        #print "-" * 40
        #print "qdata1 %r,qaddr1 %r" % (qdata1,qaddr1)
        #print "reqa a rdat %s" % reqa.a.rdata
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
            return self.data1
        else:
            search = SearchDns(self.data)
            bb=search.run()
            cache1.set(dns.getdomain(),dns.gettype(),bb)
            return bb

if  __name__ == "__main__":
    HOST, PORT = "0.0.0.0" , 53
    server = ThreadUDPServer((HOST,PORT),ThreadUDPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()




