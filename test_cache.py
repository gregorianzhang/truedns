import unittest
import truedns2

class mytest1(unittest.TestCase):
    def setUp(self):
        self.tclass = truedns2.DnsCache()

    def tearDown(self):
        pass

    def testcheckcache(self):
        self.assertEqual(self.tclass.check('www.bbb.com','a'),1)

class mytest(unittest.TestCase):
    def setUp(self):
        self.tclass = truedns2.DnsCache()

    def tearDown(self):
        pass

    def testcheckcache(self):
        self.assertEqual(self.tclass.check('www.bbb.com','a'),1)

    def testadd(self):
        self.tclass.set('www.bbb.com','a','tttt')
        self.assertEqual('tttt',self.tclass.cache['www.bbb.com_a'])





if __name__ == '__main__':
    unittest.main()
