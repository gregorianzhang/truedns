#!/usr/bin/python

from lib.conf.config import conf

def main():

	print "main"
	#conf("truedns.py")
	aa = conf("truedns.conf1")
	aa.openconf()

if __name__ == "__main__":
	main()
