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
        self.loginPage = QWidget()
        self.menuPage = QWidget()
        self.loadPage = QWidget()
        self.calcPage = QWidget()
        self.animationPage = QWidget()
        self.completePage = QWidget()
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
 
    def uploadHelper(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Text files (*.txt)")[0]
        print(fileName)
        positions = parseManifest(fileName)
        print(positions)

    def loginFunc(self):
        self.widgetStack.setCurrentIndex(0)

        layout = QFormLayout(self.loginPage)
        textfield = QLineEdit()
        layout.addRow("Name",textfield)
        loginBtn = QPushButton('Login')
        layout.addWidget(loginBtn)

        loginBtn.clicked.connect(self.menuFunc)
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(1)
        layout = QGridLayout(self.menuPage)

        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginFunc)
        loadBtn = QPushButton('Onload/Offload')
        loadBtn.clicked.connect(self.loadFunc)
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(lambda: self.calcFunc(jobType=0))
        contBtn = QPushButton('Continue')
        contBtn.clicked.connect(lambda: self.animationFunc(cont=self.cont))
        '''
        loginBtn.setStyleSheet("padding: 5em;")
        balanceBtn.setStyleSheet("padding: 5em;")
        loadBtn.setStyleSheet("padding: 5em;")
        contBtn.setStyleSheet("padding: 5em;")
        '''
        
        layout.addWidget(loginBtn)
        layout.addWidget(loadBtn)
        layout.addWidget(balanceBtn)
        layout.addWidget(contBtn)

    def loadFunc(self):
        self.widgetStack.setCurrentIndex(2)
        self.uploadHelper()
        layout = QGridLayout(self.loadPage)
        testBtn = QPushButton('Run')
        testBtn.clicked.connect(lambda: self.animationFunc(cont=self.cont))
        layout.addWidget(testBtn)


    '''
    Input: job type (0 for unload/offload, 1 for balance)
    '''
    def calcFunc(self, jobType):
        self.widgetStack.setCurrentIndex(3)
        fileName = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Text files (*.txt)")
        #positions = parseManifest(filename)
        layout = QVBoxLayout(self.calcPage)

        progLabel = QLabel(self.calcPage)
        progLabel.setText('Calculating...')
        progLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(progLabel)

        progBar = QProgressBar(self.calcPage)
        maxProg = 100
        progBar.setMaximum(maxProg)
        layout.addWidget(progBar)

        testBtn = QPushButton('Proceed')
        testBtn.clicked.connect(lambda: self.animationFunc(cont=self.cont))
        testBtn.setEnabled(False)
        layout.addWidget(testBtn)

        for i in range(maxProg):
            time.sleep(0.01)
            progBar.setValue(i+1)
            QApplication.processEvents()
        testBtn.setEnabled(True)
            

    def animationFunc(self, cont):
        self.widgetStack.setCurrentIndex(4)
        layout = QGridLayout(self.animationPage)
        testBtn = QPushButton('Complete operation')
        testBtn.clicked.connect(self.completeFunc)
        layout.addWidget(testBtn)

    def completeFunc(self):
        self.widgetStack.setCurrentIndex(5)
        layout = QGridLayout(self.completePage)
        
        progLabel = QLabel(self.completePage)
        progLabel.setText('All operations have been completed')
        progLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(progLabel)

        okBtn = QPushButton('OK')
        okBtn.clicked.connect(self.menuFunc)
        layout.addWidget(okBtn)


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
