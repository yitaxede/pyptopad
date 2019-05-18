#!/usr/bin/python
import base64
from os import urandom
from time import time

from nacl import pwhash, secret

from pygost.gost3412 import GOST3412Kuznechik
from pygost.gost34112012512 import pbkdf2
from pygost.gost3413 import cfb_decrypt
from pygost.gost3413 import cfb_encrypt

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class GOST_Cryptor:
    """
    GOST 34.12-2015 128-bit block cipher Kuznechik
    """
    IV_SIZE = 32

    def __init__(self, key):
        self.ciph = GOST3412Kuznechik(key)

    def encrypt(self, plaintext):
        iv = urandom(self.IV_SIZE)
        return iv + cfb_encrypt(self.ciph.encrypt, 16, plaintext, iv)

    def decrypt(self, ciphertext):
        return cfb_decrypt(self.ciph.encrypt, 16,
                           ciphertext[self.IV_SIZE:],
                           ciphertext[:self.IV_SIZE])


# SEC_MODE must be CHAR '0', '1' or '2'
#               or INT 0, 1 or 2
class Cryptor:
    """
    The crypto part of the pyptopad
    USAGE:
    Open existing database:
    c = Cryptor()
    c.open("db.ppdb")
    plaintext = c.read("password")
    c.write("string that you want to write")
    c.close()

    Create new database:
    c = Cryptor()
    c.create("db.ppdb", "password", '2')
    c.write("string that you want to write")
    c.close()
    """
    SALT_SIZE = 32  # bytes
    KEY_SIZE = 32  # bytes
    CRYPTOR_NUM = 3

    def __init__(self):
        self.salts = [None for i in range(self.CRYPTOR_NUM)]
        self.cryptors = [None for i in range(self.CRYPTOR_NUM)]

    def to_bytes(self, s):
        """
        Save conversion from string to bytes

        If the given argument is of bytes type already,
        everything still works.

        Parameters
        ----------
        s :  str or bytes

        Returns:
        ----------
        bytes :
           Converted string
           If conversion fails, an exception is raised
        """
        if isinstance(s, bytes):
            return s
        elif isinstance(s, str):
            return s.encode()
        else:
            raise TypeError("Cannot convert to bytes!")

    def to_str(self, b):
        """
        Save conversion from bytes to string

        If the given argument is of string type already,
        everything still works.

        Parameters
        ----------
        b :  bytes or str

        Returns:
        ----------
        str :
           Converted bytes
           If conversion fails, an exception is raised
        """
        if isinstance(b, str):
            return b
        elif isinstance(b, bytes):
            return b.decode()
        else:
            raise TypeError("Cannot convert to string!")

    def create(self, file_name, password, sec_mode=1):
        """
        Create new database

        Parameters
        ----------
        file_name :  str
        password : str or bytes
        sec_mode=1 : str '0', '1', '2' or int 0, 1, 2


        """
        if (sec_mode == '0' or sec_mode == 0):
            self.SEC_MODE = '0'
        elif (sec_mode == '1' or sec_mode == 1):
            self.SEC_MODE = '1'
        elif (sec_mode == '2' or sec_mode == 2):
            self.SEC_MODE = '2'
        else:
            raise TypeError("'sec_mode must be 0, 1 or 2!")

        # create file
        self.db_file = open(file_name, "wb+")
        # write SEC_MODE
        self.db_file.write(self.to_bytes(self.SEC_MODE))

        # generate and write salts
        for i in range(self.CRYPTOR_NUM):
            self.salts[i] = urandom(self.SALT_SIZE)
            self.db_file.write(self.salts[i])

        self.init_cryptors(self.to_bytes(password))

    def open(self, file_name):
        """
        Open the database file

        This function must be called
        before attempting to decrypt.
        """
        self.db_file = open(file_name, "rb+")

    def close(self):
        """
        Close the database file

        This function must be called
        after the work is done.
        """
        self.db_file.close()

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext

        Note that self.init_cryptors() must be called
        before calling this function.

        Parameters
        ----------
        plaintext :  str or bytes

        Returns:
        ----------
        bytes
           Ciphertext
           If encryption fails, an exception is raised
        """
        ciphertext = self.to_bytes(plaintext)

        for i in range(self.CRYPTOR_NUM):
            ciphertext = self.cryptors[i].encrypt(ciphertext)

        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext

        Note that self.init_cryptors() must be called
        before calling this function.

        Parameters
        ----------
        ciphertext :  bytes

        Returns:
        ----------
        str
           Decrypted plaintext
           If decryption fails, an exception is raised
        """
        plaintext = ciphertext

        for i in reversed(range(self.CRYPTOR_NUM)):
            plaintext = self.cryptors[i].decrypt(plaintext)

        return plaintext

    def read(self, password):
        """
        Read the database

        Read SEC_MODE, salts and encrypted database,
        then try to decrypt it.

        Parameters
        ----------
        password : string or bytes

        Returns:
        ----------
        str
           Decrypted plaintext
           If decryption fails, an exception is raised
        """
        # read SEC_MODE
        self.db_file.seek(0)
        self.SEC_MODE = self.to_str(self.db_file.read(1))

        # read salts
        for i in range(self.CRYPTOR_NUM):
            self.salts[i] = self.db_file.read(self.SALT_SIZE)

        ciphertext = self.db_file.read()

        self.init_cryptors(password)
        plaintext = self.decrypt(ciphertext)

        return self.to_str(plaintext)

    def write(self, plaintext):
        """
        Write the plaintext in the open database

        Old content of database will be destroyed,
        while sec_mode and salts are preserved.

        Parameters
        ----------
        plaintext : string or bytes
        """
        # erase old ciphertext
        self.db_file.seek(1 + self.SALT_SIZE * self.CRYPTOR_NUM)
        self.db_file.truncate()

        self.db_file.write(self.encrypt(plaintext))

    def init_cryptors(self, password):
        """
        Initialize the cryptors according to the given sec_mode

        This function must be called before
        trying to encrypt/decrypt anything.

        Parameters
        ----------
        password : string or bytes
        """
        password = self.to_bytes(password)

        kdfs = [None for i in range(self.CRYPTOR_NUM)]
        KEYS_SIZE = self.KEY_SIZE * self.CRYPTOR_NUM

        if self.SEC_MODE == '0':
            nacl_ops = pwhash.argon2i.OPSLIMIT_INTERACTIVE
            nacl_mem = pwhash.argon2i.MEMLIMIT_INTERACTIVE
            gost_iters = 4
            crypt_iters = 60000
        elif self.SEC_MODE == '1':
            nacl_ops = pwhash.argon2i.OPSLIMIT_MODERATE
            nacl_mem = pwhash.argon2i.MEMLIMIT_MODERATE
            gost_iters = 24
            crypt_iters = 500000
        elif self.SEC_MODE == '2':
            nacl_ops = pwhash.argon2i.OPSLIMIT_SENSITIVE
            nacl_mem = pwhash.argon2i.MEMLIMIT_SENSITIVE
            gost_iters = 111
            crypt_iters = 2500000
        else:
            raise TypeError("Wrong SEC_MODE!")

        kdfs[0] = lambda pw: pwhash.argon2i.kdf(
                    KEYS_SIZE,
                    pw, self.salts[0][:pwhash.argon2i.SALTBYTES],
                    opslimit=nacl_ops, memlimit=nacl_mem)

        kdfs[1] = lambda pw: pbkdf2(pw, self.salts[1], gost_iters, KEYS_SIZE)

        kdfs[2] = lambda pw: PBKDF2HMAC(
                                        algorithm=hashes.SHA256(),
                                        length=KEYS_SIZE,
                                        salt=self.salts[2],
                                        iterations=crypt_iters,
                                        backend=default_backend()
                             ).derive(pw)

        long_key = password
        for i in range(self.CRYPTOR_NUM):
            long_key = kdfs[i](long_key)

        keys = [long_key[self.KEY_SIZE * i: self.KEY_SIZE * (i+1)]
                for i in range(self.CRYPTOR_NUM)]

        self.cryptors[0] = Fernet(base64.urlsafe_b64encode(keys[2]))
        self.cryptors[1] = GOST_Cryptor(keys[1])
        self.cryptors[2] = secret.SecretBox(keys[0])


def benchmark(sec_mode):
    """
    Test perfomance of various security modes on this device

    Parameters
    ----------
    sec_mode : str '0', '1', '2' or int 0, 1, 2

    Returns:
    ----------
    float
        Time in seconds for key initialization
    """
    c = Cryptor()

    if (sec_mode == '0' or sec_mode == 0):
        c.SEC_MODE = '0'
    elif (sec_mode == '1' or sec_mode == 1):
        c.SEC_MODE = '1'
    elif (sec_mode == '2' or sec_mode == 2):
        c.SEC_MODE = '2'
    else:
        raise TypeError("'sec_mode must be 0, 1 or 2!")

    c.salts = [bytes(str(i)*c.SALT_SIZE, "utf-8")
               for i in range(c.CRYPTOR_NUM)]

    t = time()
    c.init_cryptors(b'weak_password')
    return time() - t


'''
    Benchmark result 1 (old laptop):
0.33399415016174316
0.3794994354248047
0.4099159240722656
sec_mode 0 :  1.1285181045532227
1.9901113510131836
2.2889082431793213
2.186595916748047
sec_mode 1 :  6.470615386962891
10.72014307975769
10.585609197616577
10.949737310409546
sec_mode 2 :  32.26047968864441

    Benchmark result 2 (average laptop):
0.07126164436340332
0.18033599853515625
0.170609712600708
sec_mode 0 :  0.42421579360961914
0.4363086223602295
1.123704433441162
0.8865206241607666
sec_mode 1 :  2.450796365737915
3.055706739425659
5.368149042129517
4.387252569198608
sec_mode 2 :  12.813369512557983

    Benchmark result 3 (new air laptop):
0.1626896858215332
0.41172027587890625
0.4547615051269531
sec_mode 0 :  1.033708095550537
0.9779727458953857
2.5290307998657227
2.3286056518554688
sec_mode 1 :  5.839951753616333
5.319471597671509
11.855222225189209
11.731590747833252
sec_mode 2 :  28.910637378692627
'''
