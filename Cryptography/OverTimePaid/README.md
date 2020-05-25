# Over Time: Paid

## Cryptography: 50 points

## Solve

After many months of hard work by our agents, we've gained access to a sensitive payroll document from a competitor. Unfortunately, it looks heavily encrypted. [document.encrypted](./document.encrypted) [source.py](./source.py)

## Hints

* Isn't it strange how each line of text in their document is of an identical length?
* Key Management is a difficult problem on the battlefield; maybe they reused key material in this document?
* Previous documents we've recovered had lines of encrypted whitespace as a result of text-formatting in the plaintext... Maybe that applies to this document too?


## Solution

Reviewing the source code shows that the OTP is just a 64 byte string. The encoding algorithm XORs each byte with a corresponding byte in the OTP and loops for the entire length of the string to encrypt. To reverse this, run it through the same XOR function; a decryption function is not needed.

The next step is to find the OTP used in the original encrypted file. A known string is needed to XOR with the encrypted data to produce the OTP. This is similar to The Imitation Game where the code breakers use a known phrase to decrypt the key. In this case, the phrase `The following encoded individuals are to be given a $27.3k bonus` is standard text used in every encrypted message. It also contains 64 characters, conveniently matching the key length. This phrase can be used to produce the key.

The full decryption code is in [OverTimePaid.py](./OverTimePaid.py). The output is in [output.txt](./output.txt)

## Python Byte Encoding Notes
If a byte is within the ascii range, python prints it out like normal. If it is not, python prints it in the format `\x00`, where 00 is the two hex digits that represent the byte. Take the following byte string:
```
b')\x88m\xa3\xa92x\x18c\xca\xdb\xd0Y\x9d\xa2q' 
```

The first 10 bytes are:
```
1)  open parenthesis ')'. 
2)  \x88 
3)  m
4)  \xA3
5)  \xA9
6)  2
7)  x
8)  \x18
9)  x
10) \xCA
```