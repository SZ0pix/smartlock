import datetime
import logging

    #take current time
now = datetime.datetime.now()
global i
i=0


#ENTRIES
    # create logger
loggerEntries = logging.getLogger(__name__)
loggerEntries.setLevel(logging.INFO)
    #create handler for file
f_handlerEntries = []
f_handlerEntries.append(logging.FileHandler("logs/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y"))))
f_handlerEntries[i].setLevel(logging.INFO)
    #create formatter for handler
f_format = logging.Formatter('%(asctime)s - %(message)s')
f_handlerEntries[i].setFormatter(f_format)
    #add handler to logger
loggerEntries.addHandler(f_handlerEntries[0])

def configure():
    global i
    i+=1
    now = datetime.datetime.now()
    f_handlerEntries.append(logging.FileHandler("logs/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y"))))
    f_handlerEntries[i].setLevel(logging.INFO)
    # create formatter for handler
    f_handlerEntries[i].setFormatter(f_format)
    # add handler to logger
    loggerEntries.addHandler(f_handlerEntries[i])
    loggerEntries.removeHandler(f_handlerEntries[i-1])

def write_log(data):                #create log depending from frame (for arduino board use)
    try:
        if (data[0] == 0 and data[1] == 0 and data[2] == 9):
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
        
def write_log_mechanic():                #create log depending from frame (for arduino board use)
    try:
        loggerEntries.info('SPECIAL ACCESS FOR MECHANINS.')
    except:
        pass


def write_password(data):           # create log about new passcode
    try:
        loggerEnroll.info(f'New password: {data}')
    except:
        pass


def read_log(month,year):           # read entrance logs
    try:
        f = open("logs/SmartLockLogLogging-"+month+" {}.log".format(str(year)),'r')
        line = f.read().splitlines()            #open file, read and return text
        f.close()
        return line
    except:
        pass