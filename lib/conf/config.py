#!/usr/bin/python

class conf(object):

	def __init__(self,filename=None):
		self.filename=filename
		print "init conf class %s"  % self.filename

	def openconf(self,filename=None):
		#self.filename=filename

		print " open conf class %s"  % self.filename
		try:
			with open(self.filename) as f:
				dd=f.read()
			print dd
			f.close()
		except IOError:
			print "IO ERROR %s" % IOError
		print " open conf class %s"  % self.filename
			
