#!/usr/bin/python3
import argparse
import socket
import base64

def encodeFromBinary(binary, format):
    if format == "raw":
        print(f"binary {binary}")
        n = int(binary, 2)
        n = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return n
    if format == "b64":        
        return base64.b64encode(binary).decode('ascii')
    if format == "hex":
        return hex(int(binary, 2))[2:]
    if format == "dec":
        return str(int(binary, 2))
    if format == "oct":
        return oct(int(binary, 2))[2:]
    if format == "bin":
        return binary[2:]

def decodeToBinary(source, format):
    if format == "raw":
        return bin(int.from_bytes(source.encode(), 'big'))
    if format == "b64":
        return base64.b64decode(source)
    if format == "hex":
        return bin(int(source, 16))[2:].zfill(8)
    if format == "dec":
        return bin(int(source, 10))
    if format == "oct":
        return bin(int(source, 8))
    if format == "bin":
        return '0b' + source

def translate(source, fromType, toType):
    temp = decodeToBinary(source, fromType)
    print(f"SOURCE: {source}")
    print(f"TEMP: {temp}")
    return encodeFromBinary(temp, toType)

def testDecodeEncode(source, format):
    answer = decodeToBinary(source, format)
    print(f"SOURCE: {source}")
    print(f"ANSWER: {answer}")
    answer = encodeFromBinary(answer, format)    
    if source == answer:
        print(f"PASS: {source}, {format} decoded/encoded successful!")
    else:
        print(f"FAIL: {source}, {format} encoded/decoded to: {answer}")

def testSuite():
    testDecodeEncode("hello", "raw")
    testDecodeEncode("SGVsbG9Xb3JsZA==", "b64")
    testDecodeEncode("48656c6", "hex")
    testDecodeEncode("123456789", "dec")
    testDecodeEncode("144", "oct")
    testDecodeEncode("0b0101", "bin")
    answer = translate("YEIw==", "b64", "bin")
    expectedAnswer = "100010001110010010111010111111111111"
    if answer == expectedAnswer:
        print("PASS: Translate b64 to bin successful!")
    else:
        print(f"FAIL: Translate b64 to bin failed! \nExpected: [{expectedAnswer}]\n  Answer: [{answer}]\n type: [{type(answer)}]")

answer = translate("1110110011110000111010101100100010110000111101101011001010010110101000000111000011100010011010001110101010111000101011001100010010110110010111100111110011101010111101001001010001100110101000001101111010010010100001101001000010110100011100000111111010111110011010101110001011110100110011000111100011000100011101000101100011001010110001000101000001100110010010100101110001100010100000101011101010011010111101001001100011000110101000001010101010111100011101100101011010001100100101001011001010010010110101100111000", "bin", "dec")
print(f"ANSWER: {answer}")
# testSuite()
exit()

# 'argparse' is a very useful library for building python tools that are easy
# to use from the command line.  It greatly simplifies the input validation
# and "usage" prompts which really help when trying to debug your own code.
parser = argparse.ArgumentParser(description="Solver for 'All Your Base' challenge")
parser.add_argument("ip", help="IP (or hostname) of remote instance")
parser.add_argument("port", type=int, help="port for remote instance")
args = parser.parse_args()

# This tells the computer that we want a new TCP "socket"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This says we want to connect to the given IP and port
sock.connect((args.ip, args.port))

# This gives us a file-like view for receiving data from the connection which
# makes handling messages from the server easier since it handles the
# buffering of lines for you.  Note that this only helps us on receiving data
# from the server and we still need to send data over the underlying socket
# (i.e. `sock.send(...)` at the end of the loop below).
f = sock.makefile()


lineNumber = 0
currentFormat = ""
wantedFormat = ""
answer = ""

while True:
    line = f.readline().strip()
    # This iterates over data from the server a line at a time.  This can
    # cause some unexpected behavior like not seeing "prompts" until after
    # you've sent a reply for it (for example, you won't see "answer:" for
    # this problem). However, you can still "sock.send" below to transmit data
    # and the server will handle it correctly.

    # Handle the information from the server to extact the problem and build
    # the answer string.
    
    #pass # Fill this in with your logic
    
    # A good starting point for approaching the problem:
    #   1) Identify and capture the text of each question (the "----" lines
    #          should be useful for this).
    #   2) Extract the three primary parts of each question:
    #      a) The source encoding
    #      b) The destination encoding
    #      c) The source data
    #   3) Convert the source data to some "standard" encoding (like 'raw')
    #   4) Convert the "standardized" data to the destination encoding    
    if lineNumber == 1:    
        # [format] -> [format] line
        formats = line.split()
        # print(line)
        # print(f"format1: {formats[0]}, format2: {formats[2]}")
        currentFormat = formats[0]
        wantedFormat = formats[2]
        lineNumber += 1
    elif lineNumber == 2:
        # We are now on the line containing the source data
        print(f"CURRENT LINE: [{line}]")
        answer = translate(line, currentFormat, wantedFormat)        
        break

    # check for dashed line
    if "-----" in line:
        lineNumber += 1


    if line == "":
        pass    
    else:
        print(line)

# Send a response back to the server    
print(f"Answer: [{answer}]")
sock.send((answer + "\n").encode()) # The "\n" is important for the server's
                                    # interpretation of your answer, so make
                                    # sure there is only one sent for each
                                    # answer.

f = sock.makefile()
while True:
    line = f.readline().strip()