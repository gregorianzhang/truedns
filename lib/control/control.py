import logging
from lib.server import server

class control(object):
    def __init__(self):
	pass

    def run(self):
	logging.debug('start control')
	print "aaaaa"
	t = server.server()
	print t
	t.server()
	
	
