#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys

continue_reading = True
no_tag = True
last_token = ''
flag = 0

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()

token_command = {
                "3d:99:38:62:fe": "reset", 
                "ac:26:f3:15:6c": "forward",
                "80:46:a0:90:f6": "right",
                "1c:3a:f2:15:c1": "left",
                "cc:e5:f2:15:ce": "flush",
                "2c:7f:f0:15:b6": "x2",
                "5c:9d:ef:15:3b": "x3",
                "fc:20:f3:15:3a": "x5",
                "8c:10:f1:15:78": "x8"
                }

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        token = ':'.join('{:02x}'.format(a) for a in uid)
        no_tag = False
        flag = 0
        if last_token != token:
            last_token = token
            print token_command[token]
            sys.stdout.flush()

    else:
        if no_tag == False and len(last_token) != 0 and flag == 0:
            flag = flag + 1
        elif no_tag == False:
            no_tag = True
            last_token = ''
            print ''        

    time.sleep(0.2)

    

