# Lockbox

## Solve
We developed this password-protected program which uses a super-secure, military-grade hash function with 256-bits of security to ensure only someone with the proper password can print the flag.

## Hints
You do not need to crack the password.
Tools like ghidra are helpful when strings isn't enough.
Looking at calls to printf and puts is probably a good place to start.

## Solution
Download the lockbox binary file. Inspect it

$ file lockbox
lockbox: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=1b089e3c03c5c7a5d44b608bb4b7e9dc73d9ad21, not stripped

Try running the lockbox binary:

$ ./lockbox
bash: ./lockbox: Permission denied

Need to add execute permissions:

$ chmod +x lockbox
$ ls -la
-rwxrwxr-x 1 zionperez zionperez 9024 May  2 11:27 lockbox

Now run it:

$ ./lockbox  
Enter the password to get the flag: MyPassword
Wrong password so no flag for you!

Now open up lockbox in Radare2 with write permission:

$ r2 -w lockbox
[0x00000830]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Check for objc references
[x] Check for vtables
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information
[x] Use -AA or aaaa to perform additional experimental analysis.

Analyze function list:

[0x00000830]> afl
0x00000830    1 42           entry0
0x00000860    4 50   -> 40   sym.deregister_tm_clones
0x000008a0    4 66   -> 57   sym.register_tm_clones
0x000008f0    5 58   -> 51   sym.__do_global_dtors_aux
0x00000930    1 10           entry.init0
0x00000b10    1 2            sym.__libc_csu_fini
0x00000b14    1 9            sym._fini
0x00000aa0    4 101          sym.__libc_csu_init
0x0000093a    8 352          main
0x00000768    3 23           sym._init
0x00000790    1 6            sym.imp.printf
0x000007a0    1 6            sym.imp.puts
0x00000000    3 97   -> 123  loc.imp.__gmon_start
0x000007b0    1 6            sym.imp.fgets
0x000007c0    1 6            sym.imp.strlen
0x000007d0    1 6            sym.imp.SHA256_Final
0x000007e0    1 6            sym.imp.__stack_chk_fail
0x000007f0    1 6            sym.imp.memcmp
0x00000800    1 6            sym.imp.SHA256_Update
0x00000810    1 6            sym.imp.SHA256_Init

Go to the 'main' function

[0x00000830]> s main

Enter visual mode.

> V

Press 'p' a few times to go to assembly mode. Press 'c' to view your cursor.

Notice that at address 0xA22, the assembly 'je 0xa84' checks if the test comparing the password to the hash is equal. The code 'je 0xA84' will jump to 0xA84 if the passwords match. Let's change this to jump if the passwords do not match:

Move your cursor over address 0xA22 (the "je0xa37" line). Type colon ':' then enter command 'wa jne 0xA84'. The command 'wa' stands for "write assembly" and 'jne' stands for "jump if not equal."

:> wa jne 0xA84

Hit enter and exit radare. Run the lockbox program again.
$ ./lockboxEdited 
Enter the password to get the flag: password
flag: ACI{c0de_has_mil_grade_crypto}


