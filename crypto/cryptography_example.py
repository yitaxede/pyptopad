import base64
from os import urandom
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

'''
PBKDF2HMAC time depending on iterations

Iters       Time
20000       0.030s
40000       0.060s
80000       0.121s
160000      0.241s
320000      0.479s
640000 	    0.959s
1280000     1.915s
2560000     3.843s
5120000     7.675s
'''

password = "password"
salt = urandom(16)

plaintext = "A really secret message. Not for prying eyes."


kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)


key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
cipher_suite = Fernet(key)
encrypted = cipher_suite.encrypt(plaintext.encode())
decrypted = cipher_suite.decrypt(encrypted)
print(decrypted)
