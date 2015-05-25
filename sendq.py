import dnslib
import threading
import socket
import time

server = (('8.8.8.8',53),('208.67.222.222',53),('209.244.0.3',53))

class client1(object):
    def __init__(self,server,qname):
        #self.server = server
        self.qname = qname
        self.qa = ""
        self.black = ('74.125.127.102', '74.125.155.102', '74.125.39.102', '74.125.39.113', '189.163.17.5', '209.85.229.138', '249.129.46.48', '128.121.126.139', '159.106.121.75', '169.132.13.103', '192.67.198.6', '202.106.1.2', '202.181.7.85', '203.161.230.171', '203.98.7.65', '207.12.88.98', '208.56.31.43', '209.145.54.50', '209.220.30.174', '209.36.73.33', '211.94.66.147', '213.169.251.35', '216.221.188.182', '216.234.179.13', '243.185.187.39', '37.61.54.158', '4.36.66.178', '46.82.174.68', '59.24.3.173', '64.33.88.161', '64.33.99.47', '64.66.163.251', '65.104.202.252', '65.160.219.113', '66.45.252.237', '72.14.205.104', '72.14.205.99', '78.16.49.15', '8.7.198.45', '93.46.8.89',)

    def search(self,server):
        dnsserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dnsserver.settimeout(5)
        qdata = dnslib.DNSRecord.question(self.qname,"A")
        print "qdata %s" % str(qdata.pack())
        print server
        dnsserver.sendto(str(qdata.pack()),server)
        query=1
        start = time.time()
        while query:
            print "1"
            end = time.time()
            if (end-start) > 5 :
                print "time %s" % (end-start)
                query = 0
            else:
                try:
                    qdata1, qaddr1 = dnsserver.recvfrom(2048)
                    reqip = dnslib.DNSRecord.parse(qdata1)
                    print  "qdata1 %r and ip %s" % (qdata1,reqip.a.rdata)
                    #if str(reqip.a.rdata) in self.black:
                    #    print "qdata1 %r and ip %s" % (qdata1,reqip.a.rdata)
                except:
                   pass



if __name__ == '__main__':
    dd=client1(server,'zh.wikipedia.org')
    #print server[0]
    dd.search(server[0])
