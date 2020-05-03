# All Your Base Are Belong to Us - Points: 50

#!/usr/bin/python3
import argparse
import socket
import base64
import binascii


def testDecode():
    print("Testing all decodes..")
    
    expected = b'helloworld'

    # Raw
    temp = decodeToRaw("helloworld", "raw")
    assert(type(temp) == type(b'00'))
    assert(temp == expected)
    print(f"{temp}")

    # b64
    temp = decodeToRaw("aGVsbG93b3JsZA==", "b64")
    assert(temp == expected)
    print(f"{temp}")

    # hex
    temp = decodeToRaw("68656C6C6F776F726C64", "hex")
    assert(temp == expected)
    print(f"{temp}")

    # dec
    temp = decodeToRaw("492997048111900109466724", "dec")
    assert(temp == expected)
    print(f"{temp}")

    # oct
    temp = decodeToRaw("150312661543367355734466144", "oct")    
    assert(temp == expected)
    print(f"{temp}")

    # bin
    temp = decodeToRaw("01101000011001010110110001101100011011110111011101101111011100100110110001100100", "bin")
    assert(temp == expected)
    print(f"{temp}")

def decodeToRaw(source, format):
    if format == "raw":
        return source.encode()
    if format == "b64":
        return base64.b64decode(source)
    if format == "hex":
        return binascii.unhexlify(source)
    if format == "dec":
        n = int(source)
        n = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        return n
    if format == "oct":
        n = int(source, 8)
        n = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        return n
    if format == "bin":
        n = int(source, 2)
        n = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        return n

def testEncode():
    print("Testing all encodes..")
    
    source = b'helloworld'

    # Raw
    temp = encodeFromRaw(source, "raw")
    assert(temp == source.decode())
    print(f"{temp}")

    # b64
    temp = encodeFromRaw(source, "b64")
    assert(temp == "aGVsbG93b3JsZA==")
    print(f"{temp}")

    # hex
    temp = encodeFromRaw(source, "hex")
    assert(temp.upper() == "68656C6C6F776F726C64")
    print(f"{temp}")

    # dec
    temp = encodeFromRaw(source, "dec")
    assert(temp == "492997048111900109466724")
    print(f"{temp}")

    # oct
    temp = encodeFromRaw(source, "oct")    
    assert(temp == "150312661543367355734466144")
    print(f"{temp}")

    # bin
    temp = encodeFromRaw(source, "bin")
    assert(temp == "1101000011001010110110001101100011011110111011101101111011100100110110001100100")
    print(f"{temp}")

def encodeFromRaw(raw, format):
    if format == "raw":    
        return raw.decode()
    if format == "b64":        
        return base64.b64encode(raw).decode('ascii')
    if format == "hex":
        temp = int.from_bytes(raw, "big")        
        temp = hex(temp)[2:]
        return temp
    if format == "dec":        
        return str(int.from_bytes(raw, "big"))
    if format == "oct":
        return oct(int.from_bytes(raw, "big"))[2:]
    if format == "bin":
        temp = bin(int.from_bytes(raw, "big"))[2:]
        return temp

def translate(source, fromType, toType):
    temp = decodeToRaw(source, fromType)
    print(f"SOURCE: {source}")
    print(f"TEMP: {temp}")
    return encodeFromRaw(temp, toType)

testDecode()
testEncode()

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

# States
# 0 = No dashed line detected. Waiting for first dashed line
# 1 = First dashed line detected
# 2 = [src] -> [answer] line
# 3 = source text
# 4 = 2nd dashed line detected. Send answer
state = 0

while True:    
    line = f.readline().strip()
    # This iterates over data from the server a line at a time.  This can
    # cause some unexpected behavior like not seeing "prompts" until after
    # you've sent a reply for it (for example, you won't see "answer:" for
    # this problem). However, you can still "sock.send" below to transmit data
    # and the server will handle it correctly.

    # Handle the information from the server to extact the problem and build
    # the answer string.
    
    if line != "":
        print(line)

    # Check if on dashed line. If yes, increment state
    if "-----" in line and state == 0:
        state = 1 # First dashed line detected

    # Deal with current state
    if state == 1:
        # On dashed line. Increment state
        state = 2
    elif state == 2:
        # take in [src] -> [answer] data        
        formats = line.split()        
        currentFormat = formats[0]
        wantedFormat = formats[2]
        # increment state
        state = 3
    elif state == 3:
        # take in source text         
        print(f"SRC/FROM/TO: {line}, {currentFormat}, {wantedFormat}")
        answer = translate(line, currentFormat, wantedFormat)        
        # increment state
        state = 4
    elif state == 4:
        # confirm that we are on the dashed line
        assert("-----" in line, f"Error: expected to be on dashed line. Currently on line: {line}")        
        # Send a response back to the server                
        # The "\n" is important for the server's interpretation of your answer, so make
        # sure there is only one sent for each answer.        
        print(f"Sending answer: {answer}")
        sock.send((answer + "\n").encode())         
        # Reset state
        state = 0 
           
    
