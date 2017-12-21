# Requires Adafruit_Python_PN532

import binascii
import socket
import time
import signal
import sys
import urllib2

URL = 'https://visitors-dev.w3-969.ibm.com/api/rfid?number={0}'

f = req)
for x in f:
    print(x)
f.close()


import Adafruit_PN532 as PN532

# PN532 configuration for a Raspberry Pi GPIO:

# GPIO 18, pin 12
CS   = 18
# GPIO 23, pin 16
MOSI = 23
# GPIO 24, pin 18
MISO = 24
# GPIO 25, pin 22
SCLK = 25

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Number of seconds to delay after reading data.
DELAY = 0.5

# Prefix, aka header from the card
HEADER = b'BG'

def close(signal, frame):
        sys.exit(0)

signal.signal(signal.SIGINT, close)

# Create and initialize an instance of the PN532 class
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

print('PN532 NFC RFID 13.56MHz Card Reader')
while True:
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue
    # Found a card, now try to read block 4 to detect the block type
    print('')
    print(URL.format(binascii.hexlify(uid)))

    # Authenticate and read block 4
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B, CARD_KEY):
        urllib2.urlopen(urllib2.Request(URL.format(binascii.hexlify(uid))))
        continue
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        urllib2.urlopen(urllib2.Request(URL.format(binascii.hexlify(uid))))
        continue
    # Check the header
    if data[0:2] !=  HEADER:
        urllib2.urlopen(urllib2.Request(URL.format(binascii.hexlify(uid))))
        continue
    # Parse out the block type and subtype
        urllib2.urlopen(urllib2.Request(URL.format(int(data[2:8].decode("utf-8"), 16))))
    time.sleep(DELAY);