#!/usr/bin/env python3
from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes

import sys
import zlib
import binascii

'''
Firmware class encapsulates all the information needed to
create a firmware image. It is also responsible for actually
generating the image
'''

DEBUG = True
NONCE = b'\x61\x61' # 61 = 'a' in ASCII
KEY = NONCE * 8

print(f"Nonce: {NONCE}, size: {len(NONCE)}")
print(f"Key: {KEY}, size: {len(KEY)}")

class firmware(object):
    def __init__(self):
        self.revision = '2'
        self.name = 'V.i.r.t.u.a.l.K.E.Y'
        self.vin = ''
        self.user_title = ''

        self.firmware_code = open("./car_code.bin", "rb").read()[0:64]
        self.aes_key = None
        self.device_key = open("./flag", "r").read()
        print(f"Device key: {self.device_key}")

    def generate_image(self):
        img = "Rev:%s::Vin:%s::DeviceKey:%s::Name:%s::User_Title:%s::Code:%s" % (
                                           self.revision,
                                           self.vin,
                                           self.device_key,
                                           self.name,
                                           self.user_title,
                                           self.firmware_code)
        #sys.stderr.write(img)
        #sys.stderr.write("\n")
        print(f"img: {img}")
        compressed_img = zlib.compress(img.encode('utf-8'), level=9)

        if DEBUG:
            # Use default nonce 0xAA when in debug mode
            cipher = AES.new(self.aes_key, AES.MODE_GCM, NONCE)
        else:
            cipher = AES.new(self.aes_key, AES.MODE_GCM)
            print(f"Nonce: {cipher.nonce.hex()}")
        final, tag = cipher.encrypt_and_digest(compressed_img)
        
        print(f"tag: {tag.hex()}")
        #sys.stderr.write("Legnth: %s" % len(final))

        if (len(final) > 229):
            print("[X] Fatal Error: Final Firmware Image too large: (%d bytes)" % len(final))
            sys.stdout.flush()
            return

        return final

class firmware_server(object):
    def __init__(self):
        self.flag = open("./flag", "rb").read()
        if DEBUG:
            self.aes_key = KEY
        else:
            self.aes_key = get_random_bytes(16)
        print(f"AES key: {self.aes_key}")

        self.fw = firmware()
        self.final_img = None

    def handle_create_firmware(self):
        self.fw.aes_key = self.aes_key

        print("Enter Vehicle VIN: ")
        vin = input()

        if not vin.isalnum() or len(vin) != 17:
            print("Invalid VIN")
            return

        self.fw.vin = vin

        print("Vehicle Name (Blank for default):")
        name = input()

        if name == '':
            name = "My Car"

        self.fw.user_title = name

        print("Reflash Code? (y/n)")
        code = input()

        if code == 'n':
            self.fw.firmware_code = ''

        f = self.fw.generate_image()
        self.final_img = f
        print("Firmware Created Succesfully")
        sys.stdout.flush()

    def decrypt_firmware(self):
        # Unhexlify firmware image
        try:
            print("Input HEX Encoded Firmware: ")
            fw_img = input()
            fw_img = binascii.unhexlify(fw_img)            
        except Exception as e:
            print(f"Error unhexlifying firmware image: {e}")
            return

        # Unhexlify nonce
        try:
            print("Input Encryption Nonce: ")
            nonce = input()
            nonce = binascii.unhexlify(nonce)
        except Exception as e:
            print(f"Error unhexlifying nonce: {e}")
            return

        # Unhexlify tag
        try: 
            print("Input Tag: ")
            tag = input()
            tag = binascii.unhexlify(tag)
        except Exception as e:
            print(f"Error when unhexlifying tag: {e}")
            return

        try:
            cipher = AES.new(self.aes_key, AES.MODE_GCM, nonce=nonce)
            compressed = cipher.decrypt_and_verify(fw_img, tag)
        except Exception as e:
            print(f"Error decrypting firmware: {e}")            
            return

        try:
            plain = zlib.decompress(compressed)
        except:
            print("Decompressing Failed")
            return

        return plain

    def handle_read_firmware(self):
        p = self.decrypt_firmware()

        if not p:
            return
        print(p)

    def handle_write_firmware(self):
        if not self.final_img:
            print("Firmware Image not created yet!")
            return

        print(binascii.hexlify(self.final_img))

    def serve(self):
        while True:
            print(MENU)
            msg = input()

            if msg.startswith("1"):
                self.handle_create_firmware()
            elif msg.startswith("2"):
                self.handle_read_firmware()
            elif msg.startswith("3"):
                self.handle_write_firmware()
            else:
                pass



# -----------------------------------------------
#          V.I.R.T.U.A.L.K.E.Y

#            ___________ @ @
#           /         (@\   @
#           \___________/  _@
#                     @  _/@ \_____
#                      @/ \__/-="="`
#                       \_ /
#                        <|
#                        <|
#                        <|
#                        `|

#          V.I.R.T.U.A.L.K.E.Y
# -----------------------------------------------
MENU = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
1. Create New Firmware
2. Read Firmware
3. Write Firmware
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

if __name__ == '__main__':
    s = firmware_server()
    s.serve()
