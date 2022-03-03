import datetime
import logging
import random
from logging import handlers

#create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#create handler for file
f_handler = logging.FileHandler("logs/Passwords.log")
f_handler.setLevel(logging.INFO)

#create formatter for handler
f_format = logging.Formatter('%(message)s')
f_handler.setFormatter(f_format)

#add handler to logger
logger.addHandler(f_handler)

def newpass():
#draws number from 0000 to 9999 then converts it into
#4sign string, and sends it to function "check_previous"
#to check wheter this number was used recently
    number = random.randint(0, 9999)
    newpass_str=str(number)
    if len(newpass_str)==1:
        newpass_str="000"+newpass_str
    elif len(newpass_str)==2:
        newpass_str = "00" + newpass_str
    elif len(newpass_str) == 3:
        newpass_str = "0" + newpass_str
    else:
        newpass_str = newpass_str
    check_previous(newpass_str)

def check_current():
#checks last password in file with passwords and returns it
    try:
        f = open("logs/Passwords.log", 'r')
        line = f.read().splitlines()
        current_password: str=line[(len(line)-1)]
        f.close()
        return current_password
    except:
        pass

def check_previous(c):
#opens file where previous passcode are written and
#checks if recently drawn number was used recently
#if so, it calls "newpass" function to draw new one
#in other case writes new passcode to file
    try:
        f = open("logs/Passwords.log", 'r')
        line = f.read().splitlines()
        if ((len(line)) <= 10):
            length=len(line)
        else:
            length=10
        flag = 1
        for x in range(length):
           if c!=line[-(length)]:flag *= 1
           elif c=='8816':flag *= 1
           else:flag *= 0
        f.close()
    except:
        f.close()
    if(flag==1):
        logger.info(c)
    else:
        newpass()