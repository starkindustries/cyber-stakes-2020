# Speak Plainly

## Cryptography -- 150 points

### Description

There's something suspicious about how account logins happen on this server... ? http://challenge.acictf.com:12437

### Hints

* Your username and the secret strongtoken are the only components of the encrypted cookie
* How does the length of your username effect the length of the cookie?
* It is possible to guess strongtoken one byte-at-a-time because of how AES-ECB works
* The strongtoken itself does not contain any ';' characters

### Solution
On the website's index page, it states: 
> STRONGTOKEN HARDENED: We append a secret token before encrypting. Even if our AES keys are stolen, hackers cannot forge credentials!

Then on the profile page:
> If you find a way to hack our "StrongToken", submit it via the form below to get a Flag!

Finally, the hint reveals:
> Your username and the secret strongtoken are the only components of the encrypted cookie

Thus, the goal is to first grab the encrypted cookie, find the "strong token" and then submit it to get the flag.

To get the cookie, navigate to the homepage and open Chrome dev tools. Click the *Network* tab, check the *Preserve log* option, and create a new account. The username and password can be completely blank and a new account will still be created. In the *Filter* text field, enter `method:POST` to search the HTTP post request that created the account.

![Screenshot](./screenshot1.png)

[AES Electronic Codebook (ECB)][1] uses a 16 byte block cipher. The input length for AES ECB needs to be a multiple of 16 bytes, otherwise padding is added.

                            0123456789ABCDEF                          0123456789ABCDEF
For example, if password is AAAAAAAAAAAAAAA (15B) and secret token is BCDEFGHIJKLMNOPQ (16B),
then they combine to
AAAAAAAAAAAAAAABCDEFGHIJKLMNOPQ <= plaintext1
and encrypt to:
479ee841e07e0bc545ea4d54ccc35f09 <= ciphertext1 block[0]
978fca40bf62e9a83a1e690aabaabacc

                              0123456789ABCDEF
If the password is changed to AAAAAAAAAAAAAAAB, then they combine to: 
AAAAAAAAAAAAAAABBCDEFGHIJKLMNOPQ <= plaintext2
and encrypt to:
479ee841e07e0bc545ea4d54ccc35f09 <= ciphertext2 block[0]
6597fd2b7378edd3f7ce7e9a90acff56 

Notice that the first 16B in plaintext1 and plaintext2 are both equal to "AAAAAAAAAAAAAAAB".
As a result, both block0's of ciphertext1 and ciphertext2 are identical.

Plugin the found secret token into the website and get the flag.

### References
* [Speak Plainly by John Hammond](https://youtu.be/f-iz_ZAS258)
* [Speak Plainly by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/speak-plainly)
* [Block Cipher Mode (Wikipedia)][1]
* [Chosen Plaintext attack on AES in ECB mode][2]

[1]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)
[2]: https://crypto.stackexchange.com/questions/42891/chosen-plaintext-attack-on-aes-in-ecb-mode