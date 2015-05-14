#/usr/bin/python
#-*- coding:utf-8 -*-

import SocketServer
import threading
import dnslib
import os

class ThreadUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        if data == 'q\n':
            os._exit(0)
        con = Controller(data)
        con.run()
        socket = self.request[1]
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        #print "response %" % response
        print "all data %r"  % self.request[0]
        #socket.sendto(response ,self.client_address)


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


class Controller(object):
    def __init__(self, data):
        self.data = data
        self.data1 = ''

    def run(self):
        dns=DnsMessage(self.data)
        cache=DnsCache()

        if cache.check(dns.getdomain(),dns.gettype()):
            self.data1 = cache.get(dns.getdomain(),dns.gettype())
            print "data1" % self.data1
        else:
            cache.set(dns.getdomain(),dns.gettype(),"eeeee")
            print "set cache"

if  __name__ == "__main__":
    HOST, PORT = "172.18.102.2" , 5311
    server = ThreadUDPServer((HOST,PORT),ThreadUDPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()




