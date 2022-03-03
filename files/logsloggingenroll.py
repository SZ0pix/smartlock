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
f_handlerEnroll = logging.FileHandler("logs/SmartLockLogUsers.log".format(now.strftime("%B 20%y")))
f_handlerEnroll.setLevel(logging.INFO)
    #create formatter for handler
f2_format = logging.Formatter('%(asctime)s   %(message)s')
f_handlerEnroll.setFormatter(f2_format)
    #add handler to logger
loggerEnroll.addHandler(f_handlerEnroll)

def write_names(id,name):            #create log about new user
    try:
        print("ID")
        print(id)
        if (len(str(id))==1):
            loggerEnroll.info(f'USER:00{id} - {name}')
        elif (len(str(id))==2):
            loggerEnroll.info(f'USER:0{id} - {name}')
        else:
            loggerEnroll.info(f'USER:{id} - {name}')

    except:
        pass
