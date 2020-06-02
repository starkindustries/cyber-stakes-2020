# All Your Base Are Belong to Us

## Miscellaneous: 50 points

## Solve

In honor of 30 years of terrible [translations](https://en.wikipedia.org/wiki/All_your_base_are_belong_to_us), we figured we'd give you a try at a series of (easier) translation problems. All you have to do is to translate bases by connecting to {{server}}:{{port}}. In case you're new to network programs, we even have some Python [starter\_code.py](./starter\_code.py) you can use.

## Hints

* You *could* do this by hand, but is it really worth that much effort?
* While we only want the final encoding, it's probably easier to break that into separate decode and encode steps for each question.
* Don't overthink 'raw' encoding...
* Your code for encoding/decoding will probably be very similar for 4 out of 6 encodings.

## Solution
Visit challenge.acictf.com:55498 in the browser:

```
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
```

The program is a command line program and the server is likely a python server. Connect via netcat:

```
$ nc challenge.acictf.com 55498
...
------------------------------------------------------------------------------
oct -> b64
134202600612542353524460555176215223147351615647042120670572544715511427146354651012566210413064055164325002404645623034133366275012667157320062163154335673242106227642141
------------------------------------------------------------------------------
answer: 
```

Draft up a python script that will connect to the server and automatically convert the given data to the desired format. The full script is here: [AllYourBase.py](AllYourBase.py). Run this script and the flag will appear when complete.