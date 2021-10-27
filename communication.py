import datetime
import logging
import oneStacked

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
#data =[9,3,0]

def startenroll():
    print('##enroll started')

def stopenroll():
    print('##enroll stopped timeout')

def analize(data):
    try:
        if (data[0] == 9 and data[1] == 1 and data[2] == 1):
            return_text='Press finger'
            #print('##Press finger')
            return(return_text)
        elif (data[0] == 9 and data[1] == 2 and data[2] == 0):
            return_text = 'Press again'
            #print('##Press again')
            return (return_text)
        elif (data[0] == 9 and data[1] == 3 and data[2] == 0):
            return_text = 'Remove'
            #print('##Remove')
            return (return_text)
        elif (data[0] == 9 and data[1] == 4):
            return_text = f'Enroll succesfull. Id {data[2]} Fill your name and press FINISH'
            #print(f'##Enroll succesfull. Id {data[2]}')
            return (return_text)
        elif (data[0] == 9 and data[1] == 5 and data[2] == 0):
            return_text = 'Fail to capture finger#1'
            #print('##Fail to capture finger#1')
            return (return_text)
        elif (data[0] == 9 and data[1] == 6 and data[2] == 0):
            return_text = 'Fail to capture finger#2'
            #print('##Fail to capture finger#2')
            return (return_text)
        elif (data[0] == 9 and data[1] == 7 and data[2] == 0):
            return_text = 'Fail to capture finger#2'
            #print('##Fail to capture finger#2')
            return (return_text)
        elif (data[0] == 9 and data[1] == 8):
            return_text = f'Error code: {data[2]}'
            #print(f'##Error code: {data[2]}')
            return (return_text)
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