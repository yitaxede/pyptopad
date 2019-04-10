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


class GOST_Cryptor:
    IV_SIZE = 32
    def __init__(self, key):
        self.ciph = GOST3412Kuznechik(key)
    def encrypt(self, plaintext):
        iv = urandom(self.IV_SIZE)
        return iv + cfb_encrypt(self.ciph.encrypt, 16, plaintext, iv)
    def decrypt(self, ciphertext):
        return cfb_decrypt(self.ciph.encrypt, 16, ciphertext[self.IV_SIZE:], ciphertext[:self.IV_SIZE])

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
    c.create("db.ppdb", "password", '2')
    c.write("string that you want to write")
    c.close()
    '''
    SALT_SIZE = 32 #bytes
    KEY_SIZE = 32
    CRYPTOR_NUM = 3
    CRYPTORS_INITED = 0
    
    salts = [None for i in range(CRYPTOR_NUM)]
    cryptors = [None for i in range(CRYPTOR_NUM)]
    
    def create(self, file_name, password, sec_mode=1):
        if (sec_mode == '0' or sec_mode == 0):
            self.SEC_MODE = '0'
        elif (sec_mode == '1' or sec_mode == 1):
            self.SEC_MODE = '1'
        elif (sec_mode == '2' or sec_mode == 2):
            self.SEC_MODE = '2'
        else:
            raise TypeError("'sec_mode must be 0, 1 or 2!")
        #create file
        self.db_file = open(file_name, "wb+")
        #write SEC_MODE
        self.SEC_MODE = sec_mode
        self.db_file.write(self.SEC_MODE.encode())
        
        
        #generate and write salts
        for i in range(self.CRYPTOR_NUM):
            self.salts[i] = urandom(self.SALT_SIZE)
            self.db_file.write(self.salts[i])
            
        self.init_cryptors(password.encode())
            
            
        
    def open(self, file_name):
        self.db_file = open(file_name, "rb+")
        
    def close(self):
        self.db_file.close()
        
    def read(self, password):
        #read SEC_MODE
        self.db_file.seek(0)
        self.SEC_MODE = self.db_file.read(1).decode()
        
        #read salts
        for i in range(self.CRYPTOR_NUM):
            self.salts[i] = self.db_file.read(self.SALT_SIZE)
        
        #read ciphertext
        #self.password = password.encode()
        ciphertext = self.db_file.read()
        #del self.password
        
        #init cryptors
        self.init_cryptors(password.encode())
        
        #try to decrypt
        plaintext = ciphertext
        for i in reversed(range(self.CRYPTOR_NUM)):
            plaintext = self.cryptors[i].decrypt(plaintext)
            
        #return decrypted plaintext
        return plaintext.decode()
        
    def write(self, plaintext):
        #clear the file
        self.db_file.seek(1 + self.SALT_SIZE * self.CRYPTOR_NUM)
        self.db_file.truncate()
        
        #encrypt
        ciphertext = plaintext.encode()
        for i in range(self.CRYPTOR_NUM):
            ciphertext = self.cryptors[i].encrypt(ciphertext)
        
        #write encrypted
        self.db_file.write(ciphertext)
        
    def init_cryptors(self, password):
        if self.CRYPTORS_INITED:
            raise Exception("Cryptors are already inited!")
        
        kdfs = [None for i in range(self.CRYPTOR_NUM)]
        KEYS_SIZE = self.KEY_SIZE * self.CRYPTOR_NUM
        
        if self.SEC_MODE == '0':
            nacl_ops = pwhash.argon2i.OPSLIMIT_INTERACTIVE
            nacl_mem = pwhash.argon2i.MEMLIMIT_INTERACTIVE
            gost_iters = 8
            crypt_iters = 150000
        elif self.SEC_MODE == '1':
            nacl_ops = pwhash.argon2i.OPSLIMIT_MODERATE
            nacl_mem = pwhash.argon2i.MEMLIMIT_MODERATE
            gost_iters = 32
            crypt_iters = 250000
        elif self.SEC_MODE == '2':
            nacl_ops = pwhash.argon2i.OPSLIMIT_SENSITIVE
            nacl_mem = pwhash.argon2i.MEMLIMIT_SENSITIVE
            gost_iters = 128
            crypt_iters = 500000
        else:
            raise TypeError("Wrong SEC_MODE!")
        
        kdfs[0] = lambda pw: pwhash.argon2i.kdf(KEYS_SIZE, 
                    pw, self.salts[0][:pwhash.argon2i.SALTBYTES], 
                    opslimit=nacl_ops, memlimit=nacl_mem)
                    
        kdfs[1] = lambda pw: pbkdf2(pw, self.salts[1], gost_iters, KEYS_SIZE)
            
        kdfs[2] = lambda pw : PBKDF2HMAC(
                                            algorithm=hashes.SHA256(),
                                            length=KEYS_SIZE,
                                            salt=self.salts[2],
                                            iterations=crypt_iters,
                                            backend=default_backend()
                                    ).derive(pw)
        
        long_key = password
        for i in range(self.CRYPTOR_NUM):
            long_key = kdfs[i](long_key)
        
        keys = [long_key[self.KEY_SIZE * i : self.KEY_SIZE * (i+1)] for i in range(self.CRYPTOR_NUM)]
        
        self.cryptors[0] = Fernet(base64.urlsafe_b64encode(keys[2]))
        self.cryptors[1] = GOST_Cryptor(keys[1])
        self.cryptors[2] = secret.SecretBox(keys[0])
        
        self.CRYPTORS_INITED = 1
        
