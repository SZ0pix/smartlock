import datetime
import logging

    #take current time
now = datetime.datetime.now()
global i
i=0

#ENROLL
    # create logger
loggerEnroll = logging.getLogger(__name__)
loggerEnroll.setLevel(logging.INFO)
    # create handler for file
f_handlerEnroll = logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogUsers.log".format(now.strftime("%B 20%y")))
f_handlerEnroll.setLevel(logging.INFO)
    #create formatter for handler
f2_format = logging.Formatter('%(asctime)s   %(message)s')
f_handlerEnroll.setFormatter(f2_format)
    #add handler to logger
loggerEnroll.addHandler(f_handlerEnroll)


#ENTRIES
    # create logger
loggerEntries = logging.getLogger(__name__)
loggerEntries.setLevel(logging.INFO)
    #create handler for file
f_handlerEntries = []
f_handlerEntries.append(logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y"))))
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
    f_handlerEntries.append(logging.FileHandler("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-{}.log".format(now.strftime("%B 20%y"))))
    f_handlerEntries[i].setLevel(logging.INFO)
    # create formatter for handler
    f_handlerEntries[i].setFormatter(f_format)
    # add handler to logger
    loggerEntries.addHandler(f_handlerEntries[i])
    loggerEntries.removeHandler(f_handlerEntries[i-1])

def write_log(data):                #create log depending from frame (for arduino board use)
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

def write_names(id,name):            #create log about new user
    try:
        if (len(str(id))==1):
            loggerEnroll.info(f'USER:00{id} - {name}')
        elif (len(str(id))==2):
            loggerEnroll.info(f'USER:0{id} - {name}')
        else:
            loggerEnroll.info(f'USER:{id} - {name}')

    except:
        pass

def write_password(data):           # create log about new passcode
    try:
        loggerEnroll.info(f'New password: {data}')
    except:
        pass


def read_log(month,year):           # read entrance logs
    try:
        f = open("C:/Users/mjszo/OneDrive/Pulpit/SmartLockLogLogging-"+month+" {}.log".format(str(year)),'r')
        line = f.read().splitlines()            #open file, read and return text
        f.close()
        return line
    except:
        pass