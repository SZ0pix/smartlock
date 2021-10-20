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

data = [0,0,999]
photoPath="C:/Users/mjszo/OneDrive/Pulpit/1/photos"
uiPath="C:/Users/mjszo/OneDrive/Pulpit/1"

Ui_Stacked,baseClass = uic.loadUiType(f"{uiPath}/stacked.ui")

logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

logger2 = logging.getLogger(__name__)

HEIGHT = 600                                                    #standard window size
WIDTH = 1024
PASSCODE = '456322'                                             #password
POSITION_X = 0
POSITION_Y = 50


class WorkerSignals(qtc.QObject):
    updateTimeSignal = qtc.pyqtSignal(str,str)

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



class MainWindow(qwt.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.ui = Ui_Stacked()
        self.ui.setupUi(self)
        self.setWindowFlags(flags)
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('First')
        self.move(POSITION_X, POSITION_Y)

        self.start()

        self.initiate()
        self.ui.button_start.setText("PRESS TO START")


        #self.switch_to_firstXD()
        self.runTask()
        time.sleep(0.5)
        self.show()


    @qtc.pyqtSlot(str,str)
    def printCurrentDataTime(self, time, date):
        self.ui.label_hour_start.setText(time)
        self.ui.label_date_start.setText(date)
        #self.ui.label_date_start.setText(time)
    # self.ui.label_hour_start.setText(text)
    #    print(f'siema {text} elo')

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
        runnalbe.signals.updateTimeSignal.connect(self.printCurrentDataTime)
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
        self.ui.button_keyBack.clicked.connect(self.start)
        self.ui.button_keyCancel.clicked.connect(self.cancel)
        self.ui.button_keySet.clicked.connect(self.settings)
        self.ui.button_start.clicked.connect(self.goToKeyboard)
        self.ui.button_access.clicked.connect(self.stopTimer)
        self.ui.button_screen.clicked.connect(self.stopTMR3)
        self.ui.button_setBack.clicked.connect(self.start)
        self.ui.button_set2.clicked.connect(self.logs)
        self.ui.button_logsBack.clicked.connect(self.start)
        self.ui.slider_month.valueChanged.connect(self.updateLog)
        self.ui.slider_year.valueChanged.connect(self.updateLog)
        self.ui.button_set1.clicked.connect(self.start_enroll)
    #@qtc.pyqtSlot(str)
    #def updateWidgetInGui(self, text):
    #    #self.ui.label_hour_start.setText(text)
    #    print(f'siema {text} elo')



    def start_enroll(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.enroll)
        self.ui.instruction.setText(communication.analize())





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
        self.ui.stackedWidget.setCurrentWidget(self.ui.keyboard)
        self.tmr4.stop()

    def checkLabel(self):
        if (len(self.number)==0):
            self.ui.label_key.setText("ENTER PASSWORD")  # show message and after 4 sec go back
        elif (len(self.number)==1):
            self.ui.label_key.setText("X")
        elif (len(self.number)==2):
            self.ui.label_key.setText("X X")
        elif (len(self.number)==3):
            self.ui.label_key.setText("X X X")
        elif (len(self.number)==4):
            self.ui.label_key.setText("X X X X")
        elif (len(self.number)==5):
            self.ui.label_key.setText("X X X X X")
        elif (len(self.number)>=6):
            self.ui.label_key.setText("X X X X X X")

    def push(self,sign):
        if (len(self.number)<=5):
            self.number += str(sign)
            print(self.number)
            self.checkLabel()
            self.checkPassword()

    def cancel(self):
        if (len(self.number)>=1):
            temp_number=list(self.number)               #create list that is equal to current input
            var1 = len(self.number) - 1                 #check length
            temp_number[var1]=''                        #set last cell in list as nothing
            self.number=''.join(temp_number)            #recreate string and sign it to self.number
            self.checkLabel()                           #update label

    def settings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings)

    def updateLog(self):
        months={1:"January" , 2:"February" , 3:"March" , 4:"April" , 5:"May" , 6:"June" , 7:"July", 8:"August",9:"September",10:"October",11:"November",12:"December"}
        number=self.ui.slider_month.value()
        searched_month=months[number]
        try:
            line=logslogging.readLog2(searched_month,self.ui.slider_year.value())
            text = ""
            for i in line:
                text+=i+'\n'
            self.ui.label.setText(text)
            self.ui.current_date_log.setText(f"{searched_month}.{self.ui.slider_year.value()}")

        except:
            text="ERROR: NO LOGS FOUND FOR THIS MONTH"
            self.ui.label.setText(text)
            self.ui.current_date_log.setText(f"{searched_month}.{self.ui.slider_year.value()}")

    def logs(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.logs)
        self.updateLog()

    def checkPassword(self):
        password_input=self.number
        if (password_input == (PASSCODE)):
            self.switch_to_third()
        elif ((len(password_input) == 6) and (password_input != PASSCODE)):
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
        self.ui.stackedWidget.setCurrentWidget(self.ui.screensaver)

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