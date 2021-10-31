#QT libraries
from PyQt5 import QtWidgets as qwt                           #basicly every GUI objects
from PyQt5 import QtCore as qtc                              #low level stuff like signals etc.
from PyQt5 import QtGui as qtg                               #fonts graphical stuff etc.
from PyQt5 import uic



#python libraries
import time
import random
import os
import datetime
import logging
import sys
#python files
import logs
import logslogging
import communication
import passwords

data = [9,3,0]
photoPath="C:/Users/mjszo/OneDrive/Pulpit/1/photos"
uiPath="C:/Users/mjszo/OneDrive/Pulpit/1"



Ui_Stacked,baseClass = uic.loadUiType(f"{uiPath}/stacked.ui")

logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

logger2 = logging.getLogger(__name__)
data = [9, 3, 0]
HEIGHT = 600                                                    #standard window size
WIDTH = 1024
#PASSCODE = '4563'                                             #password
POSITION_X = 0
POSITION_Y = 50

class WorkerSignals(qtc.QObject):
    updateTimeSignal = qtc.pyqtSignal(str,str)
    incomingDataSignal = qtc.pyqtSignal(int)

class SerialCom(qtc.QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        i = 0
        while(True):
            i += 1
            time.sleep(1)
            logger2.warning(f"Mamy {i}")
            self.update_date = datetime.datetime.today().strftime('%A, %d.%m')
            self.update_time = datetime.datetime.today().strftime('%H:%M:%S')
            self.signals.updateTimeSignal.emit(self.update_time, self.update_date)

            #self.updateWidgets.emit(self.update_time)

            #print(self.update_time)

            #self.update.emit(self.update_time)
            #self.progress.emit(i+1)
        #self.finished.emit()


class Worker2(qtc.QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()


    def run(self):
        while(True):
            number = input()
            try:
                data=int(number)
                self.signals.incomingDataSignal.emit(data)
            except:
                pass
            print(data)
            logger2.warning(f"poprzedni imput{number}")

class MainWindow(qwt.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.pixmap_key = qtg.QIcon("C:/Users/mjszo/OneDrive/Pulpit/1/graphic/setting.png")

        self.ui = Ui_Stacked()
        self.ui.setupUi(self)
        self.setWindowFlags(flags)
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('First')
        self.move(POSITION_X, POSITION_Y)

        self.start()

        self.initiate()
        self.ui.button_start.setText("PRESS TO START")

        #worke.signals.incomingDataSignal.connect(MainWindow.trigerchange)
        #self.switch_to_firstXD()
        self.runTask()
        time.sleep(0.5)
        self.show()

        #self.signals.incomingDataSignal.connect(MainWindow.trigerchange)

    @qtc.pyqtSlot(str,str)
    def printCurrentDataTime(self, time, date):
        self.ui.label_hour_start.setText(time)
        self.ui.label_date_start.setText(date)
        #self.ui.label_date_start.setText(time)
    # self.ui.label_hour_start.setText(text)
    #    print(f'siema {text} elo')

    @qtc.pyqtSlot(int)
    def trigerchange(self, d):
        logger2.warning(f"elemele {d}")
        data[1]=d
        dupa=communication.analize(data)
        print(type(dupa))
        print(dupa)
        self.ui.label_instruction_enroll.setText(dupa)
        if (data[1]==4):
            self.fill()
        else:
            print(data)
            print("TTTTTTTTTTTTTTTTTTTTTTTTTTTt")

    #@qtc.pyqtSlot(int)
    #def incomin

  #  def switch_to_firstXD(self):#
#
#         self.first_window = FirstWindow()
#         self.first_window.resize(WIDTH, HEIGHT)
#         self.first_window.setWindowTitle('First')
#         self.first_window.move(POSITION_X,POSITION_Y)
#         self.first_window.show()


    def runTask(self):
        pool = qtc.QThreadPool.globalInstance()
        runnalbe = SerialCom()
        worke = Worker2()
        runnalbe.signals.updateTimeSignal.connect(self.printCurrentDataTime)
        worke.signals.incomingDataSignal.connect(self.trigerchange)
        pool.start(worke)
        pool.start(runnalbe)



    #def runLongTask(self):
    #    self.thread = qtc.QThread()
    #    self.serialcom  = SerialCom()
    #    self.serialcom.moveToThread(self.thread)

    #    self.thread.started.conntect(self.serialcom.taks)
    #    self.serialcom.finished.connect(self.thread.quit)
    #    self.serialcom.finished.connect(self.serialcom.deleteLater)
    #    self.thread.finished.connect(self.thread.deleteLater)
    #    self.serialcom.progress.connect(self.reportProgress)
    #    self.thread.start()

#class FirstWindow(qwt.QWidget):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.ui = Ui_Stacked()
#        self.ui.setupUi(self)
#        self.setWindowFlags(flags)
#        self.start()
#        self.ui.button_start.setText("PRESS TO START")

    def initiate(self):
        self.ui.button_key1.clicked.connect(lambda: self.push(1))
        self.ui.button_key2.clicked.connect(lambda: self.push(2))
        self.ui.button_key3.clicked.connect(lambda: self.push(3))
        self.ui.button_key4.clicked.connect(lambda: self.push(4))
        self.ui.button_key5.clicked.connect(lambda: self.push(5))
        self.ui.button_key6.clicked.connect(lambda: self.push(6))
        self.ui.button_key7.clicked.connect(lambda: self.push(7))
        self.ui.button_key8.clicked.connect(lambda: self.push(8))
        self.ui.button_key9.clicked.connect(lambda: self.push(9))
        self.ui.button_key0.clicked.connect(lambda: self.push(0))
        self.ui.button_back_key.clicked.connect(self.start)
        self.ui.button_cancel_key.clicked.connect(self.cancel)
        self.ui.button_set_key.clicked.connect(self.settings)
        self.ui.button_start.clicked.connect(self.goToKeyboard)
        self.ui.button_access.clicked.connect(self.stopTimer)
        self.ui.button_screen.clicked.connect(self.stopTMR3)
        self.ui.button_back_set.clicked.connect(self.start)
        self.ui.button_2_set.clicked.connect(self.logs)
        self.ui.button_back_logs.clicked.connect(self.start)
        self.ui.slider_month_logs.valueChanged.connect(self.updateLog)
        self.ui.slider_year_logs.valueChanged.connect(self.updateLog)
        self.ui.button_1_set.clicked.connect(self.start_enroll)
        self.ui.button_3_set.clicked.connect(self.setdelay)
        self.ui.button_4_set.clicked.connect(self.generate)
        self.ui.button_5_set.clicked.connect(self.check_current_password)
        self.ui.button_set_delay.clicked.connect(self.senddelay)
        self.ui.slider_delay.valueChanged.connect(self.setdelay)
        self.ui.button_back_delay.clicked.connect(self.settings)
        self.ui.button_back_current.clicked.connect(self.settings)


        self.ui.button_finish_enroll.clicked.connect(self.finish_enroll)
        self.ui.button_clear_enroll.clicked.connect(self.cancel2)
        self.ui.button_break_enroll.clicked.connect(self.break_enroll)
        self.ui.button_A.clicked.connect(lambda: self.push2('A'))
        self.ui.button_B.clicked.connect(lambda: self.push2('B'))
        self.ui.button_C.clicked.connect(lambda: self.push2('C'))
        self.ui.button_D.clicked.connect(lambda: self.push2('D'))
        self.ui.button_E.clicked.connect(lambda: self.push2('E'))
        self.ui.button_F.clicked.connect(lambda: self.push2('F'))
        self.ui.button_G.clicked.connect(lambda: self.push2('G'))
        self.ui.button_H.clicked.connect(lambda: self.push2('H'))
        self.ui.button_I.clicked.connect(lambda: self.push2('I'))
        self.ui.button_J.clicked.connect(lambda: self.push2('J'))
        self.ui.button_K.clicked.connect(lambda: self.push2('K'))
        self.ui.button_L.clicked.connect(lambda: self.push2('L'))
        self.ui.button_M.clicked.connect(lambda: self.push2('M'))
        self.ui.button_N.clicked.connect(lambda: self.push2('N'))
        self.ui.button_O.clicked.connect(lambda: self.push2('O'))
        self.ui.button_P.clicked.connect(lambda: self.push2('P'))
        self.ui.button_R.clicked.connect(lambda: self.push2('R'))
        self.ui.button_S.clicked.connect(lambda: self.push2('S'))
        self.ui.button_T.clicked.connect(lambda: self.push2('T'))
        self.ui.button_U.clicked.connect(lambda: self.push2('U'))
        self.ui.button_W.clicked.connect(lambda: self.push2('W'))
        self.ui.button_Y.clicked.connect(lambda: self.push2('Y'))
        self.ui.button_Z.clicked.connect(lambda: self.push2('Z'))
        self.ui.button_Space.clicked.connect(lambda: self.push2(' '))

    def generate(self):
        passwords.newpass()

    def check_current_password(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.current_password)
        current_password=passwords.check_current()
        self.ui.label_current_password.setText("CURRENT PASSWORD: "+current_password)

    def setdelay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.delay)
        value = self.ui.slider_delay.value()
        self.ui.current_delay.setText(f"CURRENT VALUE: {value}s")

    def senddelay(self):
        pass

    def start_enroll(self):
        self.ui.label_data_enroll.setVisible(False)
        self.ui.scrollArea_2.setVisible(False)
        self.ui.stackedWidget.setCurrentWidget(self.ui.enroll)
        self.name = ''
        self.checkName()
        communication.startenroll()
        self.enroll()
        self.tmr6 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr6.setSingleShot(True)
        self.tmr6.timeout.connect(self.break_enroll)
        self.tmr6.start(30000)

    def enroll(self):
        print('Hi')
        communication.analize(data)

    def break_enroll(self):
        self.tmr6.stop()
        communication.stopenroll()
        self.start()

    def finish_enroll(self):
        id = 113
        name=self.name
        logslogging.writeNames(id,name)
        self.start()

    def start(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.access)
        self.tmr4 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr4.setSingleShot(True)
        self.tmr4.timeout.connect(self.switch_to_saver)
        self.tmr4.start(5000)
          # or if button is pushed

    def goToKeyboard(self):
        self.number = ''
        self.checkLabel()
        self.ui.stackedWidget.setCurrentWidget(self.ui.keyboard_key)
        #self.ui.button_set_key.setIcon(self.pixmap_key)
        self.tmr4.stop()

    def checkLabel(self):
        if (len(self.number)==0):
            self.ui.label_key.setText("ENTER PASSWORD")  # show message and after 4 sec go back
        elif (len(self.number)==1):
            self.ui.label_key.setText("X")
        elif (len(self.number)==2):
            self.ui.label_key.setText("X  X")
        elif (len(self.number)==3):
            self.ui.label_key.setText("X  X  X")
        elif (len(self.number)==4):
            self.ui.label_key.setText("X  X  X  X")
        #elif (len(self.number)==5):
        #    self.ui.label_key.setText("X X X X X")
        #elif (len(self.number)>=6):
        #    self.ui.label_key.setText("X X X X X X")

    def checkName(self):
        if (len(self.name)==0):
            self.ui.label_data_enroll.setText("YOUR NAME")  # show message and after 4 sec go back
        else:
            self.ui.label_data_enroll.setText(self.name)

    def push(self,sign):
        if (len(self.number)<=3):
            self.number += str(sign)
            print(self.number)
            self.checkLabel()
            self.checkPassword()

    def fill(self):
        print("SSS")
        self.ui.label_data_enroll.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)

    def push2(self,sign):
        if (len(self.name) <= 30):
            self.name += str(sign)
            print(self.name)
            self.checkName()

    def cancel(self):
        if (len(self.number)>=1):
            temp_number=list(self.number)               #create list that is equal to current input
            var1 = len(self.number) - 1                 #check length
            temp_number[var1]=''                        #set last cell in list as nothing
            self.number=''.join(temp_number)            #recreate string and sign it to self.number
            self.checkLabel()                           #update label

    def cancel2(self):
        if (len(self.name)>=1):
            temp_name=list(self.name)               #create list that is equal to current input
            var2 = len(self.name) - 1                 #check length
            temp_name[var2]=''                        #set last cell in list as nothing
            self.name=''.join(temp_name)            #recreate string and sign it to self.number
            self.checkName()                           #update label

    def settings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings)

    def updateLog(self):
        months={1:"January" , 2:"February" , 3:"March" , 4:"April" , 5:"May" , 6:"June" , 7:"July", 8:"August",9:"September",10:"October",11:"November",12:"December"}
        number=self.ui.slider_month_logs.value()
        searched_month=months[number]
        try:
            line=logslogging.readLog2(searched_month,self.ui.slider_year_logs.value())
            text = ""
            for i in line:
                text+=i+'\n'
            self.ui.label_logs.setText(text)
            self.ui.current_date_logs.setText(f"{searched_month}.{self.ui.slider_year_logs.value()}")

        except:
            text="ERROR: NO LOGS FOUND FOR THIS MONTH"
            self.ui.label_logs.setText(text)
            self.ui.current_date_logs.setText(f"{searched_month}.{self.ui.slider_year_logs.value()}")

    def logs(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.logs)
        self.updateLog()

    def checkPassword(self):
        password_input=self.number
        self.PASSCODE = passwords.check_current()
        if (password_input == (self.PASSCODE)):
            self.switch_to_third()
        elif ((len(password_input) == 4) and (password_input != self.PASSCODE)):
            self.switch_to_fourth()

    def switch_to_fourth(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.access_granted)
        self.ui.button_access.clicked.connect(self.stopTimer)  # or if button is pushed
        self.data = [0,999,0]
        self.Win()

    def switch_to_third(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.access_granted)
        self.ui.button_access.clicked.connect(self.stopTimer)              #or if button is pushed
        self.data=[2,999,0]
        self.Win()

    def Win(self):
        if self.data[0]==2:
            self.ui.button_access.setText("ACCESS GRANTED")  # show message and after 4 sec go back
        elif self.data[0]==0:
            self.ui.button_access.setText("ACCESS DENIED")  # show message and after 4 sec go back
        logslogging.writeLog2(self.data)
        self.tmr1 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr1.setSingleShot(True)
        self.tmr1.timeout.connect(self.start)
        self.tmr1.start(4000)

    def stopTimer(self):
       self.tmr1.stop()
       self.start()


#class SettingsWindow(qwt.QWidget):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.ui = Ui_Settings()  # load UI form folder
#        self.ui.setupUi(self)
#        self.setWindowFlags(flags)  # get rid off frames
#        self.ui.button_setBack.clicked.connect(self.switch_to_second)

 #   def switch_to_second(self):
 #       self.second_window = SecondWindow()
 #       self.second_window.move(POSITION_X,POSITION_Y)
 #       self.second_window.resize(WIDTH, HEIGHT)
 #       self.second_window.show()
 #       self.close()
    def switch_to_saver(self):
        self.timerVal = 1000
        HELPVAR=False
        self.ui.stackedWidget.setCurrentWidget(self.ui.screensaver_screen)

        self.tmr3 = qtc.QTimer()  # one shot timer for 4 seconds#
        self.tmr3.setSingleShot(True)  # start timer and in case of timeout change photo
        self.tmr3.timeout.connect(self.changePic)
        self.loadPictures()             #load pictures from path
        self.shotTimer()                #initialise timer in shot mode
        self.changePic()                #initialise picture rotation

    def stopTMR3(self):
        self.tmr3.stop()
        self.start()

    def loadPictures(self):
        self.pixlist = {}               #create dictionary
        self.number = len([file for file in os.listdir(photoPath) if os.path.isfile(os.path.join(photoPath, file))])    #count number of files(photos) in folder
        for i in range(1, self.number + 1):
            self.pixlist["pixmap" + str(i)] = qtg.QPixmap(f"{photoPath}/" + str(i) + ".jpg")           #create dictionary and load pictures to pixmap variables#

    def shotTimer(self):
        self.tmr3.start(self.timerVal)                       #start timer and in case of timeout change photo

    def changePic(self):
        pic = random.randint(1, self.number)                            #draw number from 1 to the number of loaded photos
        self.ui.label_screen.setPixmap(qtg.QPixmap(self.pixlist[f"pixmap{pic}"]))       #set photo to label
        self.shotTimer()                                            #relaunch timer


    ##def switch_to_first(self):
    #    self.first_window = FirstWindow()           #in case of touching one giant button for all window swithc to 1st
    #    self.first_window.resize(WIDTH, HEIGHT)
    #    self.first_window.move(POSITION_X,POSITION_Y)
    #    self.first_window.show()
    #    self.close()


if __name__ == '__main__':
    # ser=serial.Serial('/dev/ttyACM0',9600,timeout=1)
    # ser.flush()
    # while True :
    #
    #	if  ser.in_waiting>0:
    #		zmn=ser.readline().decode('utf-8').rstrip()
    #		zmn=int(zmn)
    #		if zmn==9:
    #			print(zmn)
    #			liczba=random.randint(1,3)
    #			print(liczba)
    #			ser.write(str(liczba).encode('utf-8'))


    app = qwt.QApplication(sys.argv)
    w = MainWindow()

    sys.exit(app.exec_())                                        #starts eventloop
    #dane = [0, 0, 999]
    #print('doszliśmy')
    #logs.writeLog(dane)