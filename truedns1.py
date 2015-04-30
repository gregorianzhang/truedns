#-*- coding:utf-8 -*-

import ConfigParser
import logging
import sys

def getfile(filename):
    config = ConfigParser.ConfigParser()
    
    if config.read(filename):
        dns = config.get('dnsserver','DNS1')
        port = config.get('dnsserver','DPORT')
        timeout = config.get('dnsserver','TIMEOUT')
        level = config.get('log','level')
    else:
        sys.exit('Not read conf file %s' % filename)

    return {'dns':dns,'port':port,'timeout':timeout,'level':level }

def main():
    print "main"
    fileconf = getfile('truedns.conf')
    print fileconf['level']


if __name__ == '__main__':
    main()

