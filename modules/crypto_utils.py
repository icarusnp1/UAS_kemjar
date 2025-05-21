# modules/crypto_utils.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64

# Load RSA Keys
with open('rsa_keys/public.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())
with open('rsa_keys/private.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

# RSA Encrypt AES Key
def encrypt_key_rsa(aes_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return base64.b64encode(encrypted_key).decode()

def decrypt_key_rsa(encrypted_key_b64):
    encrypted_key = base64.b64decode(encrypted_key_b64)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_key)

# AES Encrypt/Decrypt
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }

def aes_decrypt(enc_data, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=base64.b64decode(enc_data['nonce']))
    decrypted = cipher.decrypt_and_verify(
        base64.b64decode(enc_data['ciphertext']),
        base64.b64decode(enc_data['tag'])
    )
    return decrypted.decode()
