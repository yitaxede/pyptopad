import base64
from os import urandom
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = b"password"
salt = urandom(16)

plaintext = b"A really secret message. Not for prying eyes."
kdf = PBKDF2HMAC(
     algorithm=hashes.SHA256(),
     length=32,
     salt=salt,
     iterations=100000,
     backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password))
cipher_suite = Fernet(key)
encrypted = cipher_suite.encrypt(plaintext)
decrypted = cipher_suite.decrypt(encrypted)
print(decrypted)
