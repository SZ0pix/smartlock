#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=0.1) as arduino:
        #time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            while True:
                try:
                    if  arduino.inWaiting()>0: 
                        answer=str(arduino.readline().decode('utf-8').rstrip())
                        print(answer)
                        arduino.flushInput() #remove data after reading
                    else:
                        arduino.write((input()).encode())                       
                            
                except KeyboardInterrupt:
                    print("KeyboardInterrupt has been caught.")