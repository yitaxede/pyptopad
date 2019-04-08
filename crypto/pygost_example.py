from os import urandom
from pygost.gost3412 import GOST3412Kuznechik
from pygost.gost34112012512 import pbkdf2
from pygost.gost3413 import cfb_decrypt
from pygost.gost3413 import cfb_encrypt

# Kuznyechick cipher with CFB mode
'''
KDF time depending on iterations

Iters   Time
1       0.045s
2       0.096s
4       0.198s
8       0.399s
16      0.767s
32      1.530s
64      3.065s
128     6.117s
256     12.255s
512     24.900s
1024    48.612s
'''

iterations = 32
keysize = 32
key = pbkdf2(b"password", b"salt", iterations, keysize)
ciph = GOST3412Kuznechik(key)


# An initialization vector has different security requirements than a key, 
# so the IV usually does not need to be secret. However, in most cases, 
# it is important that an initialization vector is never reused 
# under the same key. 
# For CBC and CFB, reusing an IV leaks some information about 
# the first block of plaintext, and about any common prefix shared by 
# the two messages. 
# For OFB and CTR, reusing an IV completely destroys security.

# iv: blocksize-sized initialization vector
iv = urandom(16 * 2)

plaintext = bytearray("this is a plaintext", "utf-8")
encrypted = cfb_encrypt(ciph.encrypt, 16, plaintext, iv)

decrypted = cfb_decrypt(ciph.encrypt, 16, encrypted, iv).decode("utf-8")
print(decrypted)
