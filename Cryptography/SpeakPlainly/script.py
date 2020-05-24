#!/usr/bin/python3

import requests
from string import printable

# From the website:
#   If you find a way to hack our "StrongToken", submit it via the form below to get a Flag!
#   We append a secret token before encrypting. Even if our AES keys are stolen, hackers cannot forge credentials!

# Note: Input length for AES_ECB needs to be multiple of 16B, otherwise padding is added.

#                             0123456789ABCDEF                          0123456789ABCDEF
# For example, if password is AAAAAAAAAAAAAAA (15B) and secret token is BCDEFGHIJKLMNOPQ (16B),
# then they combine to
# AAAAAAAAAAAAAAABCDEFGHIJKLMNOPQ <= plaintext1
# and encrypt to:
# 479ee841e07e0bc545ea4d54ccc35f09 <= ciphertext1 block[0]
# 978fca40bf62e9a83a1e690aabaabacc
#
#                               0123456789ABCDEF
# If the password is changed to AAAAAAAAAAAAAAAB, then they combine to: 
# AAAAAAAAAAAAAAABBCDEFGHIJKLMNOPQ <= plaintext2
# and encrypt to:
# 479ee841e07e0bc545ea4d54ccc35f09 <= ciphertext2 block[0]
# 6597fd2b7378edd3f7ce7e9a90acff56 
#
# Notice that the first 16B in plaintext1 and plaintext2 are both equal to "AAAAAAAAAAAAAAAB".
# As a result, both block0's of ciphertext1 and ciphertext2 are identical.
#
# Plugin the found secret token into the website and get the flag:
# Correct! The Flag is: ACI{69059be12b858bf904a2d072a6a}

# This function just breaks down the auth token into 32 char block sizes
def get_cipher_blocks(auth_token):
    block_size = 32
    blocks = []
    for i in range(0, len(auth_token), block_size):
        blocks.append(auth_token[i:i+block_size])
    return blocks

def get_auth_token(username):
    data = {
        "username": username,
        "password": "password"
    }
    # Request session
    url = "http://challenge.acictf.com:12437/"
    s = requests.Session()
    s.post(url + "register", data = data)
    auth_token = s.cookies['auth_token']
    s.close()
    return get_cipher_blocks(auth_token)

if __name__ == "__main__":
    input_length = 31
    secret_token = ""    

    while input_length - len(secret_token) > 0:        
        username = "A" * (input_length - len(secret_token))
        cipher1 = get_auth_token(username)
        
        # loop through all printable characters
        for c in printable:
            guess = username + secret_token + c
            print(f"Trying username: {guess}")
            cipher2 = get_auth_token(guess)
            if cipher1[1] == cipher2[1]:
                secret_token += c
                print(f"c1: {' '.join(cipher1)}")
                print(f"c2: {' '.join(cipher2)}")
                print(f"Match found: [{c}]\nKnown token: [{secret_token}]")
                break

    print(f"Found secret token: {secret_token}")