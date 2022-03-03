import datetime


def writeLog(data):
    try:
        now = datetime.datetime.now()
        path = "C:/Users/mjszo/OneDrive/Desktop/SmartLockLog-{}.txt".format(now.strftime("%B 20%y"))
        print(path)
        file = open(path, mode='a+')

        dataToFile = now.strftime("20%y.%m.%d  %H:%M")
        if (data[0] == 0 and data[1] == 0 and data[2] == 999):
            file.writelines("{}  Access denied. Unknown user.\n".format(dataToFile))
        elif (data[0] == 0 and data[1] == 999 and data[2] == 0):
            file.writelines("{}  Access denied. Wrong code\n".format(dataToFile))
        elif data[0] == 1:
            file.writelines("{}  Access granted. Used userID={}\n".format(dataToFile, data[2]))
        elif data[0] == 2:
            file.writelines("{}  Access granted. Correct code\n")
        else:
            pass


        file.close()
    except:
        pass
