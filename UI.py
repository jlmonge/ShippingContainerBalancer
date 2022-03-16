from cgitb import text
from sqlite3 import Time
import sys
from util import *
import time

from PyQt5.QtWidgets import (
   QApplication,
   QLabel,
   QMainWindow,
   QStatusBar,
   QPushButton,
   QVBoxLayout,
   QWidget,
   QGridLayout,
   QFormLayout,
   QLineEdit,
   QStackedWidget,
   QHBoxLayout,
   QRadioButton,
   QMessageBox,
   QFileDialog,
   QProgressBar
)

from PyQt5.QtCore import Qt
 
from PyQt5.QtGui import QIcon
 
'''
PyQt5 install instructions
 
(optional) 1. python3 -m venv pyqtenv
(optional) 2. source pyqtenv/bin/activate
3. pip3 install pyqt5
'''
 
'''
window.setGeometry(100, 100, 1600, 900)
window.move(60, 15)
helloMsg = QLabel('Login', parent=window)
'''
 
 
 
class UI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        # window config
        self.title = "Keogh's Yard Portage"
        self.width = 1024
        self.height = 576
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
       
        # determine if program was unexpectedly shutdown by power outage
        self.cont = False

        # pages config
        self.calcPage = QWidget()
        layout3 = QVBoxLayout(self.calcPage)
        progLabel = QLabel(self.calcPage)
        progLabel.setText('Calculating...')
        progLabel.setAlignment(Qt.AlignCenter)
        progBar = QProgressBar(self.calcPage)
        progBar.setMaximum(100)
        progBtn = QPushButton('Proceed')
        progBtn.clicked.connect(lambda: self.animationFunc(cont=0))
        layout3.addWidget(progLabel)
        layout3.addWidget(progBar)
        layout3.addWidget(progBtn)

        self.loginPage = QWidget()
        layout0 = QFormLayout(self.loginPage)
        textfield = QLineEdit()
        layout0.addRow("Name", textfield)
        loginBtn = QPushButton('Login')
        layout0.addWidget(loginBtn)
        loginBtn.clicked.connect(lambda: self.getName(textfield))

        self.menuPage = QWidget()
        layout1 = QGridLayout(self.menuPage)
        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginFunc)
        loadBtn = QPushButton('Onload/Offload')
        loadBtn.clicked.connect(lambda: self.uploadHelper(jobType=0))
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(lambda: self.uploadHelper(jobType=1, progBar=progBar, progBtn=progBtn))
        contBtn = QPushButton('Continue')
        contBtn.clicked.connect(lambda: self.animationFunc(cont=self.cont))
        layout1.addWidget(loginBtn)
        layout1.addWidget(loadBtn)
        layout1.addWidget(balanceBtn)
        layout1.addWidget(contBtn)

        self.loadPage = QWidget()
        layout2 = QGridLayout(self.loadPage)
        testBtn = QPushButton('Run')
        testBtn.clicked.connect(lambda: self.calcFunc(jobType=0, progBar=progBar, progBtn=progBtn))
        layout2.addWidget(testBtn)   

        self.animationPage = QWidget()
        layout4 = QGridLayout(self.animationPage)
        testBtn = QPushButton('Complete operation')
        testBtn.clicked.connect(self.completeFunc)
        layout4.addWidget(testBtn)

        self.completePage = QWidget()
        layout5 = QGridLayout(self.completePage)
        progLabel = QLabel(self.completePage)
        progLabel.setText('All operations have been completed')
        progLabel.setAlignment(Qt.AlignCenter)
        okBtn = QPushButton('OK')
        okBtn.clicked.connect(self.menuFunc)
        layout5.addWidget(progLabel)
        layout5.addWidget(okBtn)

        self.widgetStack = QStackedWidget(self)
        self.widgetStack.setFixedSize(self.width, self.height)
        
        self.widgetStack.addWidget(self.loginPage)      #0
        self.widgetStack.addWidget(self.menuPage)       #1
        self.widgetStack.addWidget(self.loadPage)       #2
        self.widgetStack.addWidget(self.calcPage)       #3
        self.widgetStack.addWidget(self.animationPage)  #4
        self.widgetStack.addWidget(self.completePage)   #5

        self.loginFunc()
 
       #start at the login page
 
    def uploadHelper(self, jobType, progBar=None, progBtn=None):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Text files (*.txt)")[0]
        if fileName:
            print(fileName)
            positions = parseManifest(fileName)
            for i in positions:
                print(i)
            if jobType == 0:
                self.loadFunc()
            else:
                self.calcFunc(jobType=jobType, progBar=progBar, progBtn=progBtn)

    def loginFunc(self):
        self.widgetStack.setCurrentIndex(0)
    
    def getName(self, textfield):
        name = textfield.text()
        self.setWindowTitle(self.title + f" ({name})")

        self.menuFunc()
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(1)

    def loadFunc(self):
        self.widgetStack.setCurrentIndex(2)


    '''
    Input: job type (0 for unload/offload, 1 for balance)
    '''
    def calcFunc(self, jobType, progBar, progBtn):
        self.widgetStack.setCurrentIndex(3)
        progBar.reset()
        progBtn.setEnabled(False)

        for i in range(100):
            time.sleep(0.01)
            progBar.setValue(i+1)
            QApplication.processEvents()
        progBtn.setEnabled(True)
            

    def animationFunc(self, cont):
        self.widgetStack.setCurrentIndex(4)

    def completeFunc(self):
        self.widgetStack.setCurrentIndex(5)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    if not sys.platform.startswith('win32'):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText("Incompatible Operating System")
        msgbox.setWindowTitle("Error")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
    else:
        ui = UI()
        ui.show()
        sys.exit(app.exec_())
