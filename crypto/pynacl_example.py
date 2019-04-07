from nacl import pwhash, secret, utils

# OPSLIMIT_INTERACTIVE
# MEMLIMIT_INTERACTIVE
# OPSLIMIT_SENSITIVE
# MEMLIMIT_SENSITIVE
# OPSLIMIT_MODERATE
# MEMLIMIT_MODERATE

password = b"password shared between Alice and Bob"
message = b"This is a message for Bob's eyes only"

# argon2id?
kdf = pwhash.argon2i.kdf
salt = utils.random(pwhash.argon2i.SALTBYTES)
ops = pwhash.argon2i.OPSLIMIT_SENSITIVE
mem = pwhash.argon2i.MEMLIMIT_SENSITIVE

# or, if there is a need to use scrypt:
# kdf = pwhash.scrypt.kdf
# salt = utils.random(pwhash.scrypt.SALTBYTES)
# ops = pwhash.scrypt.OPSLIMIT_SENSITIVE
# mem = pwhash.scrypt.MEMLIMIT_SENSITIVE

key = kdf(secret.SecretBox.KEY_SIZE, password, salt,
                 opslimit=ops, memlimit=mem)
box = secret.SecretBox(key)


nonce = utils.random(secret.SecretBox.NONCE_SIZE)
encrypted = box.encrypt(message, nonce)

received = box.decrypt(encrypted)
print(received.decode('utf-8'))
