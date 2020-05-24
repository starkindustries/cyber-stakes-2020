# All Your Base Are Belong to Us

## Solve
In honor of 30 years of terrible translations, we figured we'd give you a try at a series of (easier) translation problems. All you have to do is to translate bases by connecting to challenge.acictf.com:55498. In case you're new to network programs, we even have some Python starter code you can use.

## Hints
You could do this by hand, but is it really worth that much effort?
While we only want the final encoding, it's probably easier to break that into separate decode and encode steps for each question.
Don't overthink 'raw' encoding...
Your code for encoding/decoding will probably be very similar for 4 out of 6 encodings.

## Notes
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