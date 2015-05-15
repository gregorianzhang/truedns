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
        response=str(con.run())
        socket = self.request[1]
        #cur_thread = threading.current_thread()
        #response = "{}: {}".format(cur_thread.name, data)
        #print "response %" % response
        print "all data %r"  % response
        socket.sendto(response ,self.client_address)


class ThreadUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class DnsCache(object):

    def __init__(self):
        self.cache={}

    def set(self,qname,qtype,qdata):
        self.cache[qname+"_"+qtype]=qdata

    def get(self,qname,qtype):
        return self.cache[qname+"_"+qtype]

    def check(self,qname,qtype):
        try:
            print "qname %s and qtype %s" % (qname,qtype)
            self.cache[qname+"_"+qtype]
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
        print "self.data %r" % self.data
        self.socket.sendto(self.data,self.server)

    def run(self):
        qdata1=""
        while not qdata1:
            try:
                qdata1,qaddr1 = self.socket.recvfrom(1024)
            except:
                pass
        #qdata,qaddr = self.socket.recvfrom(1024)

        print "qdata1 %r,qaddr1 %r" % (qdata1,qaddr1)
        return qdata1

        



class Controller(object):
    def __init__(self, data):
        self.data = data
        self.data1 = ''

    def run(self):
        dns=DnsMessage(self.data)
        cache=DnsCache()
        if cache.check(dns.getdomain(),dns.gettype()):
            print "1"*20
            self.data1 = cache.get(dns.getdomain(),dns.gettype())
            return self.data1
        else:
            print "2"*20
            search = SearchDns(self.data)
            bb=search.run()
            cache.set(dns.getdomain(),dns.gettype(),bb)
            print "search %r" % bb
            return bb

if  __name__ == "__main__":
    HOST, PORT = "172.18.102.2" , 5311
    server = ThreadUDPServer((HOST,PORT),ThreadUDPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()




