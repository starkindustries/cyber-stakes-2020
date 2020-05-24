#!/usr/bin/python3

from pwn import *
import string

def guess(p, guess):
    vin = '45678901234567890'
    p.recvuntil('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    p.sendline('1')
    p.sendline(vin)
    inp = '^:DeviceKey:'+guess
    # print(f"input: {inp}")
    p.sendline(inp)

    p.recvuntil('Reflash Code? (y/n)')
    p.sendline('y')
    # https://stackoverflow.com/questions/29643544/python-a-bytes-like-object-is-required-not-str
    result1 = p.recvuntil('bytes)').decode().split(':')[2].split(' ')[1].lstrip('(')
    
    print(f"result: {result1}")
    return int(result1)

p = remote('challenge.acictf.com', 45098)

length = 101


flag = ""
baseLen = guess(p, flag)
lastFoundChar = None

while lastFoundChar != ":":
    for x in ":" + '_' + string.ascii_letters + string.digits:
        p.info(f"Trying {flag + x}")
        length = guess(p, flag + x)
        if length == baseLen:
            flag += x
            lastFoundChar = x                
            p.success(f"Found character: {x}, {flag}")
            break

# for x in '_' + string.ascii_letters + string.digits + ":":
#     p.info("Trying {:s}".format(s+x))
#     res1 = guess(p,s+x)
#     if res1 < 231:
#         #ltrs.append(x)
#         p.success("Found one character: {:s}, {:s}".format(x,s))