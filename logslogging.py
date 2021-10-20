import datetime
import logging

#create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
now = datetime.datetime.now()
#create handler for file
f_handler = logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y")))
f_handler.setLevel(logging.INFO)

#create formatter for handler
f_format = logging.Formatter('%(asctime)s - %(message)s')
f_handler.setFormatter(f_format)

#add handler to logger
logger.addHandler(f_handler)

def writeLog2(data):
    try:
        if (data[0] == 0 and data[1] == 0 and data[2] == 999):
            logger.info('Access denied. Unknown user.')
        elif (data[0] == 0 and data[1] == 999 and data[2] == 0):
            logger.info('Access denied. Wrong code')
        elif data[0] == 1:
            logger.info("Access granted. Used userID={}".format(data[2]))
        elif data[0] == 2:
            logger.info("Access granted. Correct code")
        else:
            pass
    except:
        pass


def readLog2(month,year):
    try:
        f = open("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-"+month+" {}.log".format(str(year)),'r')
        line = f.read().splitlines()
        f.close()
        return line
    except:
        pass