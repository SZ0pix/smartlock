import sys
from PyQt5 import QtWidgets as qwt                           #basicly every GUI objects
from PyQt5 import QtCore as qtc                              #low level stuff like signals etc.
from PyQt5 import QtGui as qtg                               #fonts graphical stuff etc.

class ScreenSaver(qwt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## Start code here

        self.button_one = qwt.QPushButton('Start')
        self.button_one.clicked.connect(self.switch_to_second)



        ##End code here
        self.show()

    def switch_to_second:
        pass


class SecondWindow(qwt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



if __name__ == '__main__':
    app = qwt.QApplication(sys.argv)
    w = MainWindow(windowTitle='dupa dupa')
    sys.exit(app.exec_())                                        #starts eventloop