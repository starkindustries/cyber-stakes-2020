#!/usr/bin/python3
import argparse
import socket

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
# 4 = 2nd dashed line detected
# 5 = read for answer
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
        print(f"CURRENT LINE: [{line}]")
        answer = translate(line, currentFormat, wantedFormat)        
        # increment state
        state = 4
    elif state == 4:
        # confirm that we are on the dashed line
        assert("-----" in line, f"Error: expected to be on dashed line. Currently on line: {line}")
        # increment state
        state = 5
    elif state == 5:
        # Send a response back to the server
        answer = "Clearly not the answer..."
        # The "\n" is important for the server's interpretation of your answer, so make
        # sure there is only one sent for each answer.        
        sock.send((answer + "\n").encode())         
        # Reset state
        state = 0

    
