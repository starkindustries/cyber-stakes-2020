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

### Prompt
In honor of 30 years of terrible translations, we figured we'd give you a try at a series of (easier) translation problems. All you have to do is to translate bases by connecting to challenge.acictf.com:55498. In case you're new to network programs, we even have some Python starter code you can use.

### Hints
You could do this by hand, but is it really worth that much effort?
While we only want the final encoding, it's probably easier to break that into separate decode and encode steps for each question.
Don't overthink 'raw' encoding...
Your code for encoding/decoding will probably be very similar for 4 out of 6 encodings.

### Notes
Visiting challenge.acictf.com:55498 in the browser, shows:
'''

  This program is going to ask you to convert among 6 different bases a total
  of 5 times.  Each question is placed inside of lines delimited by 78
  '-' characters.  The first line of each question indicates the base we are
  giving to you as well as the base we expect the result in and looks like:
          [src_base] -> [answer base]
  The next line of the question is the source text that we want you to convert
  into the new base. Your answer should be followed by a newline character.

  All of the encodings treat an underlying printable ASCII string as a
  big-endian number.  If that doesn't make a lot of sense, don't worry about
  it: most of the tools you'd look to use (Python, websites, etc.) generally
  assume this anyways.  Except for 'raw' and 'b64', there will never be
  leading 0s at the start of the answer.

  Formatting key:
          raw = the unencoded ASCII string (contains only printable characters
                    that are not whitespace)
          b64 = standard base64 encoding (see 'base64' unix command)
          hex = hex (base 16) encoding (case insensitive)
          dec = decimal (base 10) encoding
          oct = octal (base 8) encoding
          bin = binary (base 2) encoding (should consist of ASCII '0' and '1')
    
------------------------------------------------------------------------------
raw -> hex
ff!fjitWSMh`,Yf@Gg>uxYy't/*Xvzx[%<3^<WnQnfFK)DgFC3}k'-lT44|Lo*JS
------------------------------------------------------------------------------
answer: That is incorrect.  I was expecting:
666621666a697457534d68602c59664047673e7578597927742f2a58767a785b253c335e3c576e516e66464b2944674643337d6b272d6c5434347c4c6f2a4a53

Goodbye
'''
At first, I was confused about how the webpage was receiving an answer already. I didn't post any data to the webpage. 

The key to understanding this challenge was to use Netcat. Using Netcat, it's easy to see that the program is a command line program. The server is likely a python server. 

Running
$ nc challenge.acictf.com 55498
This will show the page's prompt as normal, but this time the last line will hang waiting for user's input like this:

'''
------------------------------------------------------------------------------
oct -> b64
134202600612542353524460555176215223147351615647042120670572544715511427146354651012566210413064055164325002404645623034133366275012667157320062163154335673242106227642141
------------------------------------------------------------------------------
answer: 
'''

From this point, the python starter script made a lot more sense. The key was sending the answer at the correct moment that the server was expecting it, which is right after reading the 2nd dashed line.

## Let me INNNNNN - Points: 40
Prompt
Let's see if you can break into our secure vault.

Hints
How is the email determined for the password resending?

Notes:
Go to the Login page and inspect the login form. You'll see there is a hidden input with id="email" and value="vault.master@cyberstakes.com". Change this email to your email and click "Resent password". Check your email for the password. Enter the password and get the flag.

## Binary Exploitation 101 - Points: 50 
### Prompt
Exploiting bugs in programs can definitely be difficult. Not only do you need a certain amount of reverse engineering required to identify vulnerabilities, but you also need to weaponize that vulnerability somehow. To get new hackers started, we included our annotated source code along with the compiled program.
If you don't know where to start, download the source code and open it in a program with syntax highlighting such as notepad++ or gedit. If you don't have the ability to use either of those, you can always use vim.

You can connect to the problem at telnet challenge.acictf.com 19919 or nc challenge.acictf.com 19919

### Hints
Signed integers on modern computers generally use something called "Two's Complement" for representing them. If this is your first time dealing with integers at this level, it is probably worth taking some time to get a basic understanding of them. In particular, you will need to understand what the largest positive number looks like, what -1 looks like, and how overflow is generally "handled".

We've also included debug symbols in the binary and disabled compiler optimizations. Once you understand how the C code works from the source code, it is probably worth opening the compiled binary in something like Ghidra to see both what the assembly looks like and how the recovered C code compares to the source code. Most of the other binary exploitation problems do not give you access to the raw source code.

While many binary exploitation situations involve "non-standard" inputs (such as feeding shellcode as input to the name of something), this challenge does not. Once you understand the vulnerability, you can trigger it through normal interaction with the challenge. If you are having trouble on the math side, treating the binary representation of your 'target' number as an unsigned integer may be helpful.

If you are new to binary exploitation (or C code), we really recommend reading the source file in its entirety as the comments try to explain many of the key concepts for this category of problems. For this specific problem, anyone not familiar C should definitely read the source file because the behavior of s.numbers[-1] is very different between C and some other popular languages (e.g. Python).

### Notes
The source code tells us that the flag is stored in s.numbers[-1]. The vulnerable code lies in this line:
printf("%d * %d = %d which ends in a '%s'\r\n", first, second, tmp, s.numbers[tmp % 10]);

In s.numbers[tmp % 10], we can control the value of tmp because tmp is just the product of the two numbers we entered earlier.

So we want tmp to equal -1 so that s.numbers[-1] can give us the flag. But how can we multiply two positive numbers to get -1. This is where the two's complement hint comes in. With two's complement, you can convert any positive number to its negative complement by flipping all of its bits and then adding 1. See BenEater's video below for a great explanation. 

With this in mind, we know that -1 is equal to 1111...1111 in binary. So to get this result, we just need to multiple two numbers to get -1. An unsigned 32bit integer with all 1s is equal to 4,294,967,295. Divide this by 5 to get: 858993459. Therefore 5 and 858993459 are our two numbers. Plug these into the program and get the flag.

$ nc challenge.acictf.com 19919

Twos complement: Negative numbers in binary
https://www.youtube.com/watch?v=4qH4unVtJkE

Max Unsigned Int
https://en.wikipedia.org/wiki/4,294,967,295

## Over Time: Paid - Points: 50 

### Prompt
After many months of hard work by our agents, we've gained access to a sensitive payroll document from a competitor. Unfortunately, it looks heavily encrypted. document.encrypted source.py

### Hints
Isn't it strange how each line of text in their document is of an identical length?
Key Management is a difficult problem on the battlefield; maybe they reused key material in this document?
Previous documents we've recovered had lines of encrypted whitespace as a result of text-formatting in the plaintext... Maybe that applies to this document too?

### Notes
Reviewing the source code shows that the OTP is just a 64 byte string. The encoding algorithm XORs each byte with a corresponding byte in the OTP and loops for the entire length of the string to encrypt. To reverse this, just run it through the same XOR function; don't need to create a decryption function.

The next step is to find the OTP used in the original encrypted file. We just need a known string to XOR with the encrypted data to produce the OTP. This is similar to The Imitation Game where the code breakers use a known phrase to decrypt the key. In this case, we can see that "The following encoded individuals are to be given a $27.3k bonus" is standard text used in every encrypted message. It also contains 64 characters, conveniently matching the key length. We can use this to produce the key.

The full decryption code is in OverTimePaid.py. 

Quick note about python byte encoding. If a byte is within the ascii range, python prints it out like normal. If it is not, python prints it in the format \x00, where 00 is the two hex digits that represent the byte. Take the following byte string:
b')\x88m\xa3\xa92x\x18c\xca\xdb\xd0Y\x9d\xa2q' 
The first 10 bytes are: 
1) open parenthesis ')'. 
2) \x88 
3) m
4) \xA3
5) \xA9
6) 2
7) x
8) \x18
9) x
10) \xCA

## DENIED - Points: 75
### Prompt
Sometimes websites are afraid of the terminator finding things out. http://challenge.acictf.com:12133 The flag is in flag.txt.

### Hints
How can websites keep search engines from finding private information?
Sometimes the developers leave some comments that give you a hint about what to do...
You can use the cat command to read files

### Notes
The website hints at robots. Check the /robots.txt page to see whats there. Robots.txt contains:
'''
User-agent: *
Allow: /index.html
Allow: /products.html
Disallow: /maintenance_foo_bar_deadbeef_12345.html
'''

Maintenance seems interesting. Visiting this page you get a page that says: "Result: Run a command!" Inspecting the page and looking at the source shows a commented section:
<!--
    Disabled for being insecure... oops!
<form action="/secret_maintenance_foo_543212345", method="POST">
    <input name="cmd"/>
</form>-->

Uncommenting this section reveals an input box that you can type a command in. 'pwd', 'ls', and 'cat' are all valid commands for this input.

Using python requests library, we can post commands to /secret_maintenance_foo to experiment. The 'ls' command produces:
'''
flag.txt
robots.txt
server.py
static
templates
xinet_startup.sh
'''
Then 'cat flag.txt' produces the flag.

## Proxy List
### Prompt
We need you to perform geolocation analysis on this list of IPs. We have attributed it to a malicious proxy network. Report back with the prevalent country of origin: ips.txt

### Hints
The flag is the name of the origin country (case-sensitive) found most frequently in the list
Offline geolocation IP analysis can be scripted with a python package or two
These IPs were collected in late 2019, if necessary you may need to use 'historical' geolocation data

### Notes
Need to install geoip2 python library:
pip3 install geoip2

Need to download the GeoLite2-Country.mmdb database file:
https://www.maxmind.com/en/accounts/290137/geoip/downloads

Sample source code for geoip2:
https://geoip2.readthedocs.io/en/latest/
>>> import geoip2.database
>>>
>>> # This creates a Reader object. You should use the same object
>>> # across multiple requests as creation of it is expensive.
>>> reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
>>>
>>> # Replace "city" with the method corresponding to the database
>>> # that you are using, e.g., "country".
>>> response = reader.city('128.101.101.101')
>>>
>>> response.country.iso_code
'US'
>>> response.country.name
'United States'
>>> response.country.names['zh-CN']
u'美国'
>>>
>>> response.subdivisions.most_specific.name
'Minnesota'
>>> response.subdivisions.most_specific.iso_code
'MN'
>>>
>>> response.city.name
'Minneapolis'
>>>
>>> response.postal.code
'55455'
>>>
>>> response.location.latitude
44.9733
>>> response.location.longitude
-93.2323
>>>
>>> response.traits.network
IPv4Network('128.101.101.0/24')
>>>
>>> reader.close()

## Not So Meta - Points: 50
### Prompt
Look, it's the flag! Oh wait...it looks like we need to take a closer look... not_so_meta.jpg

### Hints
How do images keep contextual information when they're created? (e.g., GPS data, creation timestamp, etc.)
How do you encode binary data into common ASCII characters?

### Notes
Starting off with hexdump, we can see that there is some exif data stored in the jpg file. 
hexdump -C not_so_meta.jpg > not_so_meta_hex.txt

To view just the ascii bytes, we can use the 'strings' command. 
strings -n 64 not_so_meta.jpg > not_so_meta.txt

This shows a few lines of text including:
<xmp:ItsTheFlag>QUNJezhhM2E0OWJjZWUxM2MzZGNlYzE4MGQzNDgxZX0=</xmp:ItsTheFlag>

Convert that base64 string to ascii to get the flag.