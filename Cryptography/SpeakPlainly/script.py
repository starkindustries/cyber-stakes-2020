#!/usr/bin/python3

import requests
from string import printable

# Break down the auth token into 32 char block sizes
# so that individual cipher blocks can be inspected
def get_cipher_blocks(auth_token):
    block_size = 32
    blocks = []
    for i in range(0, len(auth_token), block_size):
        blocks.append(auth_token[i:i+block_size])
    return blocks

# Get the auth token (a cookie) from the challenge website
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