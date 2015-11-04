#/usr/bin/python
#-*- coding:utf-8 -*-

import SocketServer
import threading
import dnslib
import os
import sys
import socket,asyncore
import time
import struct
from Queue import Queue
from threading import Thread
import collections
import pickle


queue=Queue(5000)
#cache={}
global n 
n=0

class hijacking(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            self.hijacking = 0
            self.data = queue.get()
            #print "self.data %r" % self.data
            self.server=(('8.8.8.8',53),('208.67.220.220',53))
            for x in self.server:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socket.settimeout(5)
                #print x
                if self.hijacking == 1:
                    self.socket.close()
                    break
                self.socket.sendto(self.data,x)
                start = time.time()
                temp = []
                q =1
                while q:
                    end = time.time()
                    if (end-start)>5:
                        q = 0
                    else:
                        try:
                            qdata2, qaddr2 = self.socket.recvfrom(2048)
                            temp.append(qdata2)
                        except:
                            pass
    
                self.socket.close()
                if len(temp) > 1:
                    #print "This is hijacking dns %s" % temp
                    self.hijacking = 1
                    
                    tt = tcpdns(self.data)
                    tt.run()
                    break


class tcpdns(Thread):
    def __init__(self,data):
        #print "tcpdns init"
        self.data = data

    def run(self):
        self.server = (('8.8.4.4',53),('208.67.222.222',443))
        for x in self.server:
            #print x
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            try:
                self.socket.connect(x)
                dnslen = struct.pack('>H',len(self.data))
                self.socket.send(dnslen+self.data)
                dnsq = self.socket.recv(2048)
                reqa = dnslib.DNSRecord.parse(self.data)
                if dnsq:
                    #print "domain %s and type %s and data %r" % (reqa.q.qname,reqa.q.qtype,dnsq[2:])
                    #print "cache %s"% cache
                    #print "in here"
                    try:
                        bb= dnslib.DNSRecord.parse(dnsq[2:])
                        #print "bb %s" % bb
                    except:
                        continue

                    #print "server ip rdata %s" % bb.a.rdata
                    #print "reqa.q.qname %s" % str(reqa.q.qname)
                    #print "reqa.q.qtype %s" % str(reqa.q.qtype)
                    #print "data %s" % dnsq[2:]

                    #cache[str(reqa.q.qname)+"_"+str(reqa.q.qtype)] = dnsq[2:]
                    #print cache1
                    cache1.set(str(reqa.q.qname),str(reqa.q.qtype),dnsq[2:])
                    #print "cache domain %s and data %s "% (str(reqa.q.qname)+"_"+str(reqa.q.qtype), dnsq[2:])
                    self.socket.close()
                    #print "end"
                    break
                else:
                    pass
                    #print "dnsq is null"
                    
                #print "3" * 10
            except:
                pass
                #print "haha"
            self.socket.close()


class ThreadUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        global n       
        if data == 'q\n':
            os._exit(0)
        elif data[:2] == 'd ':
            cache1.delete(data[2:][:len(data[2:])-1])
        else:
            n += 1

        #try:
        #print "data %r" % data 
#            print "data %s" % self.request
            (h,a) = self.client_address
        #print "client addr %s %s" % (h,a)
        #except:
        #    pass
        #print n
            if n > 1000:
                cache1.save()
                n=0

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

    def __init__(self):
#	pass
        print "DnsCache init"
        self.cache = ""
        self.cache_size = 10000
        self.path = sys.path[0]
        self.open()


    def set(self,qname,qtype,qdata):
	print "set cache %s number" % len(self.cache)
        print "set qname  %s qtype %s self.cache[qname+\"_\"+qtype] %s" %(qname,qtype,qdata)
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)
        else:
            self.cache[qname+"_"+qtype]=qdata

    def delete(self,qname_qtype):
        #print "del defore cache %s number " % len(self.cache)
        #for temp_j in self.cache:
        #    print self.cache[temp_j]
        self.cache.pop(qname_qtype)
        print "del after cache %s number " % len(self.cache)
        #for temp_j in self.cache:
        #    print self.cache[temp_j]


    def get(self,qname,qtype):
	print "get cache %s number" % len(self.cache)
        value = self.cache.pop(qname+"_"+qtype)
        self.cache[qname+"_"+qtype] = value
        return self.cache[qname+"_"+qtype]

    def check(self,qname,qtype):
	#global cache
	#print "check cache %s number" % len(cache)
        #print "dnscache %s" % cache
        try:
            print "qname %s and qtype %s" % (qname,qtype)
	    print "cache len %s" % len(self.cache)
            self.cache[qname+"_"+qtype]
            return 1
        except KeyError:
            return 0

    def save(self):
	print "save cache %s number" % len(self.cache)
        with open(self.path + '/dns_cache.data_tmp','wb+') as f:
            data = pickle.dumps(self.cache)
            f.write(data)
	    os.rename(self.path + '/dns_cache.data_tmp' , self.path + '/dns_cache.data')

    def open(self):
        global data
	data = ""
        try:
            with open(self.path + '/dns_cache.data', 'rb+') as f:
                data = f.read()
            print "data len %s" % len(data)
        except UnboundLocalError, e:
            data = ''
	    print "open execpt %s" % e
            print "data is null"
        finally:

            if data == '':
                self.cache = collections.OrderedDict()
		print "open finally null  cache %s number" % len(self.cache)
                
            else:
                self.cache = pickle.loads(data)
		print "open finally cache %s number" % len(self.cache)


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
        qdata1 = ""
        queue.put(self.data)
        while not qdata1:
            try:
                qdata1, qaddr1 = self.socket.recvfrom(2048)
                reqa = dnslib.DNSRecord.parse(qdata1)
            except:
                pass

        #print "domain %s " % dir(reqa.q)
        #print "domain %s and type %s" % (reqa.q.qname,reqa.q.qtype)
        self.socket.close()
        return qdata1

#    def run(self):
#        #print "query data %r" % self.data
#        qdata1=""
#        while not qdata1:
#            try:
#                qdata1,qaddr1 = self.socket.recvfrom(2048)
#                reqa = dnslib.DNSRecord.parse(qdata1)
#
#            except:
#                pass
#
#        #print "qdata1 %r" % qdata1
#        dnss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        dnss.settimeout(5)
#        for x in self.server1:
#            #print x
#            dnss.sendto(self.data,x)
#            start = time.time()
#            temp = []
#            queue = 1
#            while queue:
#                end = time.time()
#                if (end-start)>5:
#                    queue = 0
#                else:
#                    try:
#                        qdata2, qaddr2 = dnss.recvfrom(2048)
#                        reqa = dnslib.DNSRecord.parse(qdata2)
#                        #print "udp return ip address %s" % reqa.a.rdata
#                        temp.append(qdata2)
#                    except:
#                        pass
#
#            if len(temp) > 1:
#                self.hijacking = 1
#                for x in temp[:len(temp)-1]:
#                    ip = dnslib.DNSRecord.parse(x)
#                    blacklist.append(str(ip.a.rdata))
#                break
#
#        dnsst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        dnsst.settimeout(5) 
#        for x in self.server2:
#            #print x
#            dnsst.connect(x)
#            tcpdns = struct.pack('>H',len(self.data))
#            dnsst.send(tcpdns+self.data)
#            qdata3 = dnsst.recv(2048)
#            tcpdnsq = struct.unpack('>H',qdata3[:2])
#            if tcpdnsq[0] == len(qdata3[2:]):
#                reqa = dnslib.DNSRecord.parse(qdata3[2:])
#                #print "tcp dns return ip address %s" % reqa.a.rdata
#                if reqa.a.rdata not in blacklist:
#                    break
#
#        #print blacklist
#        if self.hijacking:
#            return qdata3[2:]
#        else:
#            return qdata1

class Controller(object):
    def __init__(self, data):
        self.data = data
        self.data1 = ''

    def run(self):
        dns=DnsMessage(self.data)
        #cache1=DnsCache()
        #print cache
        n=0
        #print "cache1 %r" % cache1
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
    HOST, PORT = "172.18.102.13" , 53
    server = ThreadUDPServer((HOST,PORT),ThreadUDPRequestHandler)
    ip, port = server.server_address

    global cache1

    cache1=DnsCache()

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    bb=[]
    for x in xrange(8):
        t = hijacking()
        bb.append(t)
        t.start()

    for x in bb:
        x.join()




