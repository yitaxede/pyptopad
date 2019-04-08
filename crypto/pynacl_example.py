from nacl import pwhash, secret, utils

# OPSLIMIT_INTERACTIVE
# MEMLIMIT_INTERACTIVE
# OPSLIMIT_SENSITIVE
# MEMLIMIT_SENSITIVE
# OPSLIMIT_MODERATE
# MEMLIMIT_MODERATE

'''
                KDF comparison table
                
            INTERACTIVE     MODERATE    SENSITIVE
argon2i       0m0.439s      0m2.098s    0m11.237s
scrypt        0m0.205s      0m0.894s    0m6.716s
'''

password = b"password shared between Alice and Bob"
message = b"This is a message for Bob's eyes only"

# argon2id?
kdf = pwhash.argon2i.kdf
salt = utils.random(pwhash.argon2i.SALTBYTES)
ops = pwhash.argon2i.OPSLIMIT_INTERACTIVE
mem = pwhash.argon2i.MEMLIMIT_INTERACTIVE

# or, if there is a need to use scrypt:
# kdf = pwhash.scrypt.kdf
# salt = utils.random(pwhash.scrypt.SALTBYTES)
# ops = pwhash.scrypt.OPSLIMIT_SENSITIVE
# mem = pwhash.scrypt.MEMLIMIT_SENSITIVE

key = kdf(secret.SecretBox.KEY_SIZE, password, salt,
                 opslimit=ops, memlimit=mem)

box = secret.SecretBox(key)

encrypted = box.encrypt(message)

received = box.decrypt(encrypted)
print(received.decode('utf-8'))

