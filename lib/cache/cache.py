import logging

class cachem(object):
    cache = {}

    def __init__(self):
        pass
        

    def set(self,s1,s2,s3):
        cachem.cache[s1+'_' +str(s2)] = s3
        logging.debug('add cache key %s value %s' % ((s1+'_' +str(s2)),s3))
        logging.debug('cache is %r' % cachem.cache)
        print "cached %r" % cachem.cache

    def get(self,s1,s2):
        try:
            #return self.cachem.cahche[s1+'_' +str(s2)]
            return cachem.cache[s1+'_' +str(s2)]
        except KeyError:
            return 0

        logging.debug('get cache key %s value %s' % ((s1+'_' +str(s2)),cachem.cache[s1+'_' +str(s2)]))
        logging.debug('cache is %r' % cachem.cache[s1+'_' +str(s2)])


    def check(self,s1,s2):
        print "print s1 %s s2 %s" % (s1,s2)
        logging.debug('cache is %r' % cachem.cache)
        logging.debug('get cache key %s ' % (s1+'_' +str(s2)))
        if self.get(s1,s2):
            return 1
        else:
            return 0



