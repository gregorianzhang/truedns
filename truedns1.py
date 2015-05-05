#-*- coding:utf-8 -*-

import ConfigParser
import logging
import sys

from lib.control import control


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

    logging.basicConfig(level = logging.DEBUG,
    			format = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(name)s %(message)s",
			filename = "truedns.log",
			filemode = "a")

    fileconf = getfile('truedns.conf')
    print fileconf['level']
    logging.debug('TTTT')

    b = control.control()
    b.run()
	

if __name__ == '__main__':
    main()

