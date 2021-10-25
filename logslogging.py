import datetime
import logging

#create loggers
loggerEntries = logging.getLogger(__name__)
loggerEntries.setLevel(logging.INFO)

loggerEnroll = logging.getLogger(__name__)
loggerEnroll.setLevel(logging.INFO)

now = datetime.datetime.now()
#create handler for file
f_handlerEntries = logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y")))
f_handlerEntries.setLevel(logging.INFO)

f_handlerEnroll = logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogUsers".format(now.strftime("%B 20%y")))
f_handlerEnroll.setLevel(logging.INFO)
#create formatter for handler

f_format = logging.Formatter('%(asctime)s - %(message)s')
f_handlerEntries.setFormatter(f_format)
f_handlerEnroll.setFormatter(f_format)

#add handler to logger
loggerEntries.addHandler(f_handlerEntries)
loggerEnroll.addHandler(f_handlerEnroll)

def writeLog2(data):
    try:
        if (data[0] == 0 and data[1] == 0 and data[2] == 999):
            loggerEntries.info('Access denied. Unknown user.')
        elif (data[0] == 0 and data[1] == 999 and data[2] == 0):
            loggerEntries.info('Access denied. Wrong code')
        elif data[0] == 1:
            loggerEntries.info("Access granted. Used userID={}".format(data[2]))
        elif data[0] == 2:
            loggerEntries.info("Access granted. Correct code")
        else:
            pass
    except:
        pass


#def writeEnrollLog(id, imie):
    #try:
     #   if (data[0] == 0 and data[1] == 0 and data[2] == 999):
      #      logger.info('Access denied. Unknown user.')
       # elif (data[0] == 0 and data[1] == 999 and data[2] == 0):
      #      logger.info('Access denied. Wrong code')
       # elif data[0] == 1:
        #    logger.info("Access granted. Used userID={}".format(data[2]))
       # elif data[0] == 2:
        #    logger.info("Access granted. Correct code")
       # else:
        #    pass
    #except:
     #   pass


def readLog2(month,year):
    try:
        f = open("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-"+month+" {}.log".format(str(year)),'r')
        line = f.read().splitlines()
        f.close()
        return line
    except:
        pass