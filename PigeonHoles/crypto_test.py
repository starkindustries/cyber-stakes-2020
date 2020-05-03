#!/usr/bin/env python3
from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes
import argparse

# 'argparse' is a very useful library for building python tools that are easy
# to use from the command line.  It greatly simplifies the input validation
# and "usage" prompts which really help when trying to debug your own code.
parser = argparse.ArgumentParser(description="Solver for 'All Your Base' challenge")
parser.add_argument("plaintext", help="Plain text to be encrypted")
args = parser.parse_args()


nonce = b'\x00\x03'  # nonce needs to be 2 bytes (16 bits)
key = nonce * 8      # key needs to be 16 bytes (128 bit key-length)

def testCrypto(plaintext, key=key, nonce=nonce):
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key.hex()}")

    # Encrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    print(f"Nonce: {cipher.nonce.hex()}")
    
    hexText = ciphertext.hex()
    hexArray = [hexText[i:i+2] for i in range(0, len(hexText), 2)]
    hexString = " ".join(hexArray)
    intString = " ".join([str(int(hexChar, 16)) for hexChar in hexArray])
    
    print(f"Cipher text hex: {hexString}")
    print(f"Cipher text int: {intString}")
    print(f"Tag: {tag.hex()}")

    # Decrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decryptedtext = cipher.decrypt_and_verify(ciphertext, tag)

    print(f"Decrypted text: {decryptedtext.decode()}")


testCrypto(args.plaintext)