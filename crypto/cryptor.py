#!/usr/bin/python
import base64
from os import urandom

from nacl import pwhash, secret, utils

from pygost.gost3412 import GOST3412Kuznechik
from pygost.gost34112012512 import pbkdf2
from pygost.gost3413 import cfb_decrypt
from pygost.gost3413 import cfb_encrypt

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#SEC_MODE must be CHAR '0', '1' or '2'
class Cryptor:
    '''
    USAGE:
    c = Cryptor()
    c.open("db.ppdb")
    plaintext = c.read("password")
    c.write("string that you want to write")
    c.close()
    
    OR:
    c = Cryptor()
    c.open("db.ppdb", "password", '2')
    c.write("string that you want to write")
    c.close()
    '''
    SALT_SIZE = 32 #bytes
    CRYPTOR_NUM = 3
    
    salts = [None for i in range self.CRYPTOR_NUM]
    cryptors = [None for i in range self.CRYPTOR_NUM]
    
    def create(self, file_name, password, sec_mode='1'):
        if not sec_mode is str():
            raise TypeError("'sec_mode must be a char: '0', '1' or '2'!")
        #create file
        self.file_name = file_name
        self.db_file = open(file_name, "wb+")
        
        #write SEC_MODE
        self.SEC_MODE = sec_mode
        self.db_file.write(self.SEC_MODE)
        
        #generate and write salts
        for i in range(self.CRYPTOR_NUM):
            self.salts[i] = urandom(self.SALT_SIZE)
            self.db_file.write(self.salts[i])
            
            
        
    def open(self, file_name):
        self.db_file = open(file_name, "rb+")
        
    def close(self):
        self.db_file.close()
        
    def read(self, password):
        #read SEC_MODE
        self.file.seek(0)
        self.SEC_MODE = self.db_file.read(1)
        
        #read salts
        for i in range(self.CRYTOR_NUM):
            self.salts[i] = self.db_file.read(self.SALT_SIZE)
        
        #read ciphertext
        self.ciphertext = 
        
        
        #init cryptors
        #For NACL cryptor salt must be exactly pwhash.argon2i.SALTBYTES long (it's 16 as for today)
        self.cryptor[0] = Nacl_Cryptor(password, salts[0][:pwhash.argon2i.SALTBYTES], self.sec_mode)
        self.cryptor[1] = Gost_Cryptor(password, salts[1], self.sec_mode)
        self.cryptor[2] = Cryp_Cryptor(password, salts[2], self.sec_mode)
        
        #try to decrypt
        plaintext = self.ciphertext
        for i in reversed(range(self.CRYPTOR_NUM)):
            plaintext = self.cryptor[i].decrypt(plaintext)
            
        #return decrypted plaintext
        return plaintext
        
    def write(self, plaintext):
        #clear the file
        self.file.seek(1 + self.SALT_SIZE * self.CRYPTOR_NUM)
        self.file.truncate()
        
        #encrypt
        ciphertext = plaintext
        for i in range(self.CRYPTOR_NUM):
            ciphertext = self.cryptor[i].encrypt(ciphertext)
            
        #write encrypted
        self.file.write(ciphertext)
