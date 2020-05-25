#!/usr/bin/python3
import os
import binascii
import random

DEBUG = False

words = [
    "ALPHA",
    "BRAVO",
    "CHARLIE",
    "DELTA",
    "ECHO",
    "FOXTROT",
    "GOLF",
    "HOTEL",
    "INDIA",
    "SIERRA",
    "TANGO",
    "ZETA",
]

INTRO = "The following encoded individuals are to be given a $27.3k bonus:".ljust(63) + "\n"
OUTRO = "Furthermore, the FLAG is:".ljust(63) + "\n"

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def encrypt_otp(data, otp):
    try:
        d = data.encode('utf-8')    
    except:
        d = data
    print(f"otp: [{otp}] {type(otp)}\n")
    out = []
    for i in range(0, len(d)):
        out.append(d[i] ^ otp[i % len(otp)])
    return bytes(out)

def generate_line(length):
    out = ''
    while len(out) < length:
        out += random.choice(words) + " "

    out = out[0:length-1]
    out = ' '.join(out.split(" ")[0:-1])
    return out.ljust(length-1) + '\n'


def generate_doc(flag):
    out = INTRO

    for i in range(0,10):
        out += generate_line(64)

    out += " " * 63 + "\n"
    out += OUTRO + "\n"
    out += flag.ljust(63) + "\n"
    return out

if DEBUG:
    flag = "THIS_IS_A_SAMPLE_FLAG"
    print(f"flag: {flag}\n")
    doc = generate_doc(flag)
    print(f"doc: {doc}")
    otp = bytes(os.urandom(64))
    enc = encrypt_otp(doc, otp)
    print(f"enc: {enc}\n")
    enclist = list(divide_chunks(enc, 64))
    print(f"enc list: {enclist}\n")

    out = b''
    for line in enclist:
        out += binascii.hexlify(line) + b"\n"

    print(f"out: {out}")

    f = open("./document.encrypted", "wb")
    f.write(out)
    f.close()

###################################
# Decrypt
###################################
print("\nDECRYPT")

# Read file, remove newline chars, join string
with open("./document.encrypted", ) as file:
    lines = "".join(line.strip() for line in file)
print(lines + "\n")

# UnhexlifyFalse
unhex = binascii.unhexlify(lines)
print(f"unhex: {unhex}")
if DEBUG:
    if(unhex != enc):
        print("Error: 'unhex' and 'enc' vars do NOT match.")

# decrypt_otp
if DEBUG:
    data = encrypt_otp(unhex, otp)
    print(f"data: {data.decode('ascii')}")

# get the actual otp
key = "The following encoded individuals are to be given a $27.3k bonus"
if len(key) != 64:
    print(f"Error: expected key length 64. Received: {len(key)}")

key = key.encode('utf-8')
print(f"{key}, {type(key)}")

otp2 = encrypt_otp(unhex[0:64], key)
print(f"OTP: {otp2}")

if DEBUG:
    if(otp != otp2): 
        print(f"Error: OTPs do NOT match.\n OTP1: {otp} \n OTP2: {otp}")

# Decrypt the message
data = encrypt_otp(unhex, otp2)
print(f"data: {data.decode('ascii')}")