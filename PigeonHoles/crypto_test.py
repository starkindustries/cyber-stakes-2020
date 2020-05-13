#!/usr/bin/env python3
from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes
import argparse
import timeit
import zlib
import string

# 'argparse' is a very useful library for building python tools that are easy
# to use from the command line.  It greatly simplifies the input validation
# and "usage" prompts which really help when trying to debug your own code.
parser = argparse.ArgumentParser(description="Solver for 'All Your Base' challenge")
parser.add_argument("plaintext", help="Plain text to be encrypted")
args = parser.parse_args()


nonce = b'\x00\x00'  # nonce needs to be 2 bytes (16 bits)
key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' # key needs to be 16 bytes (128 bit key-length)


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

# Run a timing attack on the tag comparison
def runTimingAttackOnTag(plaintext):
    # Encrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    print(f"Tag: {tag.hex()}")

    tag2 = get_random_bytes(16)

    # Decrypt
    min, max = [10, -1]
    for i in range(0, 10000):
        start = timeit.default_timer()
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decryptedtext = cipher.decrypt_and_verify(ciphertext, tag2)
            print(f"Decrypted text: {decryptedtext.decode()}")
        except Exception as e:
            print(f"Error decrypting: {e}")                
        stop = timeit.default_timer()
        time = (stop - start) * 1000
        print(f"time: {time}")
        if time > max:
            max = time
        if time < min:
            min = time
    print(f"min,max: [{min}:{max}]")

def guess(img):
    compressed_img = zlib.compress(img.encode('utf-8'), level=9)
    print(f"img: {img}, len: {len(compressed_img)}")    
    # print(f"com: {compressed_img}\n")
    return len(compressed_img)

if __name__ == "__main__":
    # plaintext = args.plaintext
    # testCrypto(plaintext)
    # runTimingAttackOnTag(plaintext)

    # img = "Rev:2::Vin:45678901234567890::DeviceKey:pigeon_holes_awesome::Name:V.i.r.t.u.a.l.K.E.Y::User_Title:^:DeviceKey:this-is-the-flag::Code:car_code_123"    
    # img = "pigeon_holes_awesome::VIRTUAL_KEY::"
    realflag = "PiGe0n_40leS_1s_aWeS0m3"
    realflag = "this_1s_the_flag"
    img = "DEVICE_KEY::" + realflag + "::DATA1::" + "DEVICE_KEY::"
    baseLen = guess(img)
    print(f"base len: {baseLen}")

    flag = ""
    lastFlagChar = ""

    charList = ":" + '_' + string.ascii_letters + string.digits

    while lastFlagChar != ":":
        lastFlagChar = None
        for x in charList:
            length = guess(img + flag + x)
            if length == baseLen:
                if x == ":":
                    break
                flag += x
                lastFlagChar = x
                break
        if 

    print(f"flag: {flag}")

    # compress(img + "DEVICE_KEY::T")
    # compress(img + "DEVICE_KEY::B")
    # compress(img + "DEVICE_KEY::C")
    # compress(img + "DEVICE_KEY::D")
    # compress(img + "DEVICE_KEY::E")

    # min,max: [0.10435900185257196:2.440418000333011] for correct tag    
    # min,max: [0.10612301412038505:2.511601982405409] for wrong tag