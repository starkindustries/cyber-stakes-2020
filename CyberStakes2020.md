## InterNet Cats - Points: 4
Use netcat: $ nc \[server] \[port]
'''$ nc challenge.acictf.com 20120'''

## Out of Site - Points: 5
Inspect page and find flag in the html source.

## Rotate Me - Points: 5 
Caesar Cipher

## Filing Extension - Points: 10
We went to apply for a tax-filing extension with the IRS, and they replied with this image saying it contained the code we needed. Unfortunately, our computer refuses to display it and just says that it isn't a PNG... flag.png

First, figure out what type of file the flag is.

$ file flag.png
flag.png: Zip archive data, at least v2.0 to extract
$ unzip flag.png
Archive:  flag.png
  inflating: flag.txt  


## More Out of Site - Points: 10
Well that was embarrassing... Who knew there was more to a web site then what the browser showed? Not to worry, we're back with a new and improved Javascript version! http://challenge.acictf.com:19888

Inspect the page. Check the javascript source file for the flag.

## Bootcamp - Points: 20
We found an old floppy-drive laying around and think that there may be a flag hidden on it somewhere. We managed to copy the drive image, but there doesn't appear to be any kind of filesystem on it. In fact, all of the data appears to be on the first sector of the disk.

It looks like file floppy.img identifies it as a "DOS/MBR Boot Record"...
What happens if you try booting the image?
You probably don't have a real floppy drive that you can use, but what about a 'virtual' one?
qemu-system-i386 floppy.img is our favorite means of 'booting' floppies, but 'Virtual Box' and 'bochs' are other alternatives (and they are all free).

$ file files.tar.gz
files.tar.gz: gzip compressed data, last modified: Fri Apr 24 00:44:24 2020, from Unix
$ tar -xzvf files.tar.gz
floppy.img
$ file floppy.img
floppy.img: DOS/MBR boot sector
$ qemu-system-i386 floppy.img

## Most Out of Site - Points: 20
Alright, one more try. We had to think long and hard about how to keep you from viewing the flag. After a quick snack break, we had an epiphany. Your tricks won't work this time. http://challenge.acictf.com:54227

What on earth could snack food have to do with this problem?
The browser must be storing these cookies somewhere...
If you're getting tired of using a browser, the Python Requests library is pretty useful for interacting with web servers.

In Chrome, right click and inspect page. Click the Application tab. Under Storage, click Cookies. One of the cookies contains the flag.

## Reverse Engineering 101 - Points: 25
Reverse engineering can definitely be intimidating so we have a simple program with which you can start. If you don't know where to start, check out the hints where we'll walk you through two different ways to solve this problem.

Static analysis: Static analysis is a process for examining a program without having a computer execute any code.
* From a command line on Linux, executing objdump -d RE101 will display the assembly code for the executable sections of the program (assumes you downloaded the file to the same folder).
* Flow of this program starts at _start and proceeds 'down' the code.
objdump -t RE101 will print all of the 'symbols' in the program. These are human-readable names for specific spots in memory. Symbols in the '.text' section tend to be function names and symbols in '.bss', '.data', and '.rodata' tend to be variable names.
* You should be able to see that the address of the 'flag' symbol (second command) appears in the first instruction of the '_start' (first command).
* The hex values that are moved look like they are in the printable ASCII range.

Dynamic analysis: Dynamic analysis is a method of examining the program as it is running to learn more about what it does. A common tool to help with this is a "debugger" like gdb.
1. gdb RE101 will launch GDB and prepare it to debug our target, the RE101 executable. You may need to change the permissions on the downloaded file in order to make it executable (chmod a+x RE101).
2. break _exit will add a "breakpoint" which will pause the program's execution when we reach this point in the code. We're able to use '_exit' here as a convenience and could have also specified a memory address instead.
3. run will start execution and keep running until we hit the breakpoint we specified above.
4. x /s &flag tells GDB to 'examine' a 'string' located at the address of the 'flag' symbol ('&' is the C symbol for 'address of').

Instead of the dynamic analysis above, we could have also continued our static analysis by studying the assembly code we produced earlier. In particular, we can observe that the code is moving a pointer to the 'flag' variable into the EDI register in the first line. It then 'moves' a series of byte-constants into the memory location to which EDI points, 'incrementing' EDI in between each move. The final three lines in '_exit' execute a Linux system call to 'exit', but that is relevant for this problem.

When doing reverse engineering of x86 and x86-64 programs, Intel's instruction set reference can be very helpful. It can be intimidating to look at, but looking up the assembly instruction in this document will tell you exactly what it does.

## Really Senseless Admins - Points: 35
We fired Julius, but the new guy apparently misplaced the file with our pivate key. All he could find was the encrypted flag and some file labeled 'params'. flag.enc params.txt

The new guy apparently just treated the flag text as a big-endian integer. Apparently, this made it easier for him to use the online tools he had found.

Wouldn't it be nice if there were detailed write-ups about these cryptosystems? https://en.wikipedia.org/wiki/RSA_(cryptosystem)

We found a few notes on the admin's desk. One note just had the URL of an online RSA tool. The second note had two URLs on it with 'plaintext => hex => int' scribbled beside it. The third one makes it look like the plaintext generated by the RSA tool will start with 104. 
https://www.cryptool.org/en/cto-highlights/rsa-step-by-step
https://www.rapidtables.com/convert/number/decimal-to-hex.html

==============================
The params.txt file provides variables 'p', 'q', and 'e' for the RSA tool (cryptool.org). The flag.enc provides the ciphertext. Plug these four variables into the RSA tool.
p = 307358449224319975132699066144222436685882807714668628477464201817335216538606596193560751355060198065536448811048921551943103744796203835167959124182339648204298793067277991267869053872654998299070591661074700578450383471717960105650861723722028277409986829696857069150953926359511066023147172389630847617379

q = 303471350829576435768013789752613658823267619303280231484359795713764099787912330836505995590300214096419069232518000760901540947812817189108075444569340080872397935399647918852082970284367536780791082192877335810606026563189972788572519668502112689819584235343191091347247602987573756813840123620489201016761

e = 94455416372378889873861614626768614690502155767292925830107378277763869064397

ciphertext = 4283114025152923911035595888340045945353291052428724077240532434083672670860535988992617521390377015776218879937870762711200498375035687818319070767693653249461036430539749109643993894506898303200536554473880823517650170090081898661469775834520219111924316868780908106071680577413708819774446796182485237871731687665923919579421700002183050914259953217414121146448765745051213311484828560940385537681826693169253257132283413751573902803452471983293888690885261714683772845040171628944457788661895185413277780784467763745596879789276379145487980979785943330069579558898427407780734421225352942660821198875248580703046

On plugging these in, you get the plaintext: 
104873340459054924181115292546315913092670595907443492684969085

Following the hint "plaintext => hex => int", convert in reverse order using the conversion functions in the rapidtables site. Convert decimal to hex then hex to ASCII.

Plaintext (Decimal):
104873340459054924181115292546315913092670595907443492684969085
To Hex:
4143497B5072316D33735F54214D337A5F39636239653366347D
To ASCII:
ACI{Pr1m3s_T!M3z_9cb9e3f4}

## All Your Base Are Belong to Us
