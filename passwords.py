import datetime
import logging
import oneStacked
import random
from logging import handlers

#create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#logger_smtp = logging.getLogger(__name__)
#create handler for file
f_handler = logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/Passwords.log")
f_handler.setLevel(logging.INFO)


#smtp_handler = logging.handlers.SMTPHandler(
#                mailhost = ('smtp.gmail.com', 587),
##                fromaddr = "why.mikolaj@gmail.pl",
#                toaddrs = "why.mikolaj@gmail.pl",
#                subject = "newcode")
#smtp_handler.setLevel(logging.INFO)

#create formatter for handler
f_format = logging.Formatter('%(message)s')
f_handler.setFormatter(f_format)

#smtp_format = logging.Formatter('%(message)s')
#smtp_handler.setFormatter(smtp_format)

#add handler to logger
logger.addHandler(f_handler)
#logger_smtp.addHandler(smtp_handler)

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
        f = open("C:/Users/mjszo/OneDrive/Pulpit/Passwords.log", 'r')
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
        f = open("C:/Users/mjszo/OneDrive/Pulpit/Passwords.log", 'r')
        line = f.read().splitlines()
        if ((len(line)) <= 10):
            length=len(line)
        else:
            length=10
        flag = 1
        for x in range(length):
           if c!=line[-(length)]:flag *= 1
           else:flag *= 0
        f.close()
    except:
        f.close()
    if(flag==1):
        logger.info(c)
        #try:
            #smtp_handler.info("NOwy kod"+c)
        #except:
        #    print("NIE POSZLO")
    else:
        newpass()