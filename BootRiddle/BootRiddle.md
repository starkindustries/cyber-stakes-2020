
$ tar -xvf files.tar.gz
$ qemu-system-i386 floppy.img -monitor stdio

https://en.wikibooks.org/wiki/QEMU/Monitor

The floppy boots up with text:

Your flag awaits at 0x7DC0

Check out the 'xp' command in the wikibooks link. Use the xp command to view memory contents at that address

(qemu) xp /30c 0x7dc0
0000000000007dc0: 'A' 'C' 'I' '{' 'R' 'E' 'A' 'L' 'm' 'o' 'd' 'e' '}' '\x00' '\x00' '\x00'
0000000000007dd0: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
0000000000007de0: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
0000000000007df0: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' 'U' '\xaa'
0000000000007e00: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
0000000000007e10: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
0000000000007e20: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
0000000000007e30: '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00' '\x00'
(qemu) 

Explanation of that command:
xp /format address
xp     - Displays memory at the specified physical address using the specified format.
/30c   - Will display 30 characters. 'c' stands for char
0x7dc0 - Start at this address