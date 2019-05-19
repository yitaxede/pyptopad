#!/usr/bin/python
import unittest
from cryptor import GOST_Cryptor, Cryptor, benchmark


class TestSum(unittest.TestCase):
    key = b'8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
    plaintext = b'1122334455667700ffeeddccbbaa9988'
    def test_gost(self):

        cr = GOST_Cryptor(self.key)
        ciphertext = (cr.encrypt(self.plaintext))
        self.assertNotEqual(ciphertext, self.plaintext)
        self.assertEqual(cr.decrypt(ciphertext), self.plaintext)
    
    def test_to_bytes(self):
        cr = Cryptor()
        self.assertEqual(cr.to_bytes('some string'), b'some string')
        self.assertEqual(cr.to_bytes(b'some string'), b'some string')
    
    def test_to_str(self):
        cr = Cryptor()
        self.assertEqual(cr.to_str(b'some bytes'), 'some bytes')
        self.assertEqual(cr.to_str('some bytes'), 'some bytes')
    
    def test_crypt(self):
        cr = Cryptor()
        cr.SEC_MODE = '0'
        cr.salts = [b'0' * cr.SALT_SIZE for i in range(cr.CRYPTOR_NUM)]
        cr.init_cryptors(self.key)
        ciphertext = (cr.encrypt(self.plaintext))
        self.assertNotEqual(ciphertext, self.plaintext)
        self.assertEqual(cr.decrypt(ciphertext), self.plaintext)
        
    def test_benchmark(self):
        time0 = benchmark(0)
        time1 = benchmark(1)
        time2 = benchmark(2)
        self.assertLess(time0, time1)
        self.assertLess(time1, time2)

    def test_db(self):
        path = "/tmp/db.ppdb"
        pwd = "p@s$w0Rd"
        sec_mode = '1'
        string = "Some very secret string."
        
        cr = Cryptor()
        cr.create(path, pwd, sec_mode)
        cr.write(string)
        cr.close()

        c = Cryptor()
        c.open(path)
        plaintext = c.read(pwd)
        c.close()
        self.assertEqual(plaintext, string)


if __name__ == '__main__':
    unittest.main()
