# Speak Plainly

## Cryptography: 150 points

## Solve

There's something suspicious about how account logins happen on this server... http://challenge.acictf.com:12437

## Hints

* Your username and the secret strongtoken are the only components of the encrypted cookie
* How does the length of your username effect the length of the cookie?
* It is possible to guess strongtoken one byte-at-a-time because of how AES-ECB works
* The strongtoken itself does not contain any ';' characters

## Solution
Starting with the profile page, it gives the following prompt:
> If you find a way to hack our "StrongToken", submit it via the form below to get a Flag!

One of the hints reveals:
> Your username and the secret strongtoken are the only components of the encrypted cookie

Thus, the goal is to first grab the encrypted cookie, find the "strong token" and then submit it to get the flag.

### Get the Cookie
To get the cookie, navigate to the homepage and open Chrome dev tools. Click the **Network** tab, check the **Preserve log** option, and create a new account. The username and password fields can be completely blank and a new account will still be created. In the **Filter** text field, enter `method:POST` to search for the HTTP post request that created the account.

![Screenshot](./screenshot1.png)

There is only one POST request, which is from the `/register` page and it has a cookie called `auth_token`. This information can be used in a python script to further examine the token. The following python function will send a POST request to the `/register` page, submit a username and password, and retrieve the cookie's `auth_token`.

```
#!/usr/bin/python3
import requests


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
```

### Get the Strong Token
[AES Electronic Codebook (ECB)][1] uses a 16 byte block cipher. The input length for AES ECB needs to be a multiple of 16 bytes, otherwise padding is added. The `get_auth_token` function breaks up the `auth_token` into 16 byte blocks (32 hex characters) to easily see the block separation.

On the website's index page, it states: 
> STRONGTOKEN HARDENED: We append a secret token before encrypting. Even if our AES keys are stolen, hackers cannot forge credentials!

Again, the hint reveals that only the username and token are part of the encrypted cookie, meaning the password can be safely ignored:
> your username and the secret strongtoken are the only components of the encrypted cookie

Playing around with the input confirms this. Sending different passwords does not change the returned `auth_token` value. However, sending different usernames does.

Experimenting further, sending a username with 15 characters returns an `auth_token` with 32 bytes (64 hex characters). And sending a username with 16 characters returns an `auth_token` with 48 bytes (96 hex characters). Thus, the 16th character causes the cipher to spill over to a new block, which means that a 15 character username plus the secret `strong_token` fits into a 32 byte cipher.

Take the following hypothetical example:
```
    username: AAAAAAAAAAAAAAA   (15 bytes)
strong_token: THIS_IS_STR_TOKEN (17 bytes of unknown characters)
```
These inputs combine to create this plaintext. A space is added just to show the separation of the two 16 byte halves.
```            
plaintext1: AAAAAAAAAAAAAAAT HIS_IS_STR_TOKEN (username + strong_token)
                           ^
                           this 'T' is the 16th character
```
The character 'T' at the 16th position is also the first character of the hypothetical `strong_token`. This is intentional.

This plaintext encrypts to:
```
cipher1: a46ebd63b5e0c0c7a3f256a53a0823d2 (cipher text block 0)
         27dfd0ccf3e4868778354ee7c7b2ef49 (cipher text block 1)
```

Take a guess that the first character of the `strong_token` is 'T'. Change the username to `AAAAAAAAAAAAAAAT` (16 bytes). The username plus `strong_token` now combine to:
```
plaintext2: AAAAAAAAAAAAAAAT THIS_IS_STR_TOKEN
```
And this encrypts to:
```
cipher2: a46ebd63b5e0c0c7a3f256a53a0823d2 (cipher text block 0)
         fbbf3e20eaea58f6aeb9069ae822413f (cipher text block 1)
```

Notice that the first 16 bytes in plaintext1 and plaintext2 are both equal to `AAAAAAAAAAAAAAAT`. As a result, both cipher1 block 0 and cipher2 block 0 are equal to `a46ebd63b5e0c0c7a3f256a53a0823d2`. Therefore, 'T' is confirmed as the first character of the `strong_token`. This process can continue to reveal the entire `strong_token`. This is implemented in [script.py](./script.py).

The script starts off with 31 characters instead of 15 so that all 17 characters of the `strong_token` can be found. The [output.txt](./output.txt) file contains the entire run's output. Below is a snippet of the output file. As shown below, the script starts with 31 characters of 'A's and guesses the 32nd character.
```
Trying username: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0
Trying username: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1
Trying username: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2
...
Trying username: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;
c1: 726388a6a87eb5d7ca935884e0f8aad6 1f549bd112b7a5e82ad60b7435c22dd6 0168298f2eb15584c72075fb4eb68684
c2: 726388a6a87eb5d7ca935884e0f8aad6 1f549bd112b7a5e82ad60b7435c22dd6 fdf0b6f541181cf4fb98c94706caf42b a3b3ea76e20e07a85d330fb0ba5006f5
Match found: [;]
Known token: [;]
...
Trying username: A;J9@5:c-(rF!U:!f>*************)
Trying username: A;J9@5:c-(rF!U:!f>**************
c1: 18c1a6eea3f47f83201f91952ca90ab6 6a6c7f925f47fb7096093f5f35c4b452
c2: 18c1a6eea3f47f83201f91952ca90ab6 6a6c7f925f47fb7096093f5f35c4b452 fdf0b6f541181cf4fb98c94706caf42b a3b3ea76e20e07a85d330fb0ba5006f5
Match found: [*]
Known token: [;J9@5:c-(rF!U:!f>**************]
Found secret token: ;J9@5:c-(rF!U:!f>**************
```
Note that the asterisks '*' found are just padding for the cipher block. One of the hints mentions that the token does not have semicolons. Therefore, the `strong_token` is `J9@5:c-(rF!U:!f>`. Plug this into the profile page and get the flag.

## References
* [Speak Plainly by John Hammond](https://youtu.be/f-iz_ZAS258)
* [Speak Plainly by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/speak-plainly)
* [Block Cipher Mode (Wikipedia)][1]
* [Chosen Plaintext Attack on AES in ECB Mode][2]

[1]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)
[2]: https://crypto.stackexchange.com/questions/42891/chosen-plaintext-attack-on-aes-in-ecb-mode