from pwn import *
import string

def guess(p, guess):
    vin = '45678901234567890'
    p.recvuntil('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    p.sendline('1')
    p.sendline(vin)
    inp = '^:DeviceKey:'+guess
    p.sendline(inp)

    p.recvuntil('Reflash Code? (y/n)')
    p.sendline('y')
    result1 = p.recvuntil('bytes)').split(':')[2].split(' ')[1].lstrip('(')

    return int(result1)

p = remote('challenge.acictf.com', 45098)

length = 101

s = "ThiS_1s_th3_fl4G"

for x in '_'+string.ascii_letters+string.digits:
    p.info("Trying {:s}".format(s+x))
    res1 = guess(p,s+x)
    if res1 < 231:
        #ltrs.append(x)
        p.success("Found one character: {:s}, {:s}".format(x,s))