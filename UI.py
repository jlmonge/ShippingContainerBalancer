from cgitb import text
from sqlite3 import Time
import sys
from util import *

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
   QFileDialog
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
       
        # pages config
        self.loginPage = QWidget()
        self.menuPage = QWidget()
        self.loadPage = QWidget()
        self.progressPage = QWidget()
        self.animationPage = QWidget()
        self.widgetStack = QStackedWidget(self)
        self.widgetStack.setFixedSize(self.width, self.height)
        
        self.widgetStack.addWidget(self.loginPage)
        self.widgetStack.addWidget(self.menuPage)
        self.widgetStack.addWidget(self.loadPage)
        self.widgetStack.addWidget(self.progressPage)
        self.widgetStack.addWidget(self.animationPage)

        layout =  QVBoxLayout()
        layout.addWidget(self.widgetStack)
        self.setLayout(layout)

        self.loginFunc()
 
       #start at the login page
 
    def loginFunc(self):
        self.widgetStack.setCurrentIndex(0)

        layout = QFormLayout(self.loginPage)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(370, 200, 0, 0)

        textfield = QLineEdit()
        textfield.setMaximumWidth(200)
        textfield.setMinimumHeight(25)
        layout.addRow("Name",textfield)

        loginBtn = QPushButton('Login')
        loginBtn.setMaximumWidth(100)
        layout.addWidget(loginBtn)

        loginBtn.clicked.connect(self.menuFunc)
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(1)
        layout = QGridLayout(self.menuPage)

        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginFunc)
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(self.progressFunc)
        loadBtn = QPushButton('Onload/Offload')
        loadBtn.clicked.connect(self.loadFunc)
        contBtn = QPushButton('Continue')
        contBtn.clicked.connect(self.contFunc)

        '''
        loginBtn.setStyleSheet("min-height: 5em;")
        balanceBtn.setStyleSheet("min-height: 5em;")
        loadBtn.setStyleSheet("min-height: 5em;")
        contBtn.setStyleSheet("min-height: 5em;")
        '''

        loginBtn.setMaximumWidth(100)
        balanceBtn.setMaximumWidth(100)
        loadBtn.setMaximumWidth(100)
        contBtn.setMaximumWidth(100)
        loginBtn.setContentsMargins(0, 5, 0, 0)
        layout.setContentsMargins(360,180,0,0)
   
        layout.addWidget(loginBtn)
        layout.addWidget(balanceBtn)
        layout.addWidget(loadBtn)
        layout.addWidget(contBtn)

    def loadFunc(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Text files (*.txt)")
        #positions = parseManifest(filename)
        self.widgetStack.setCurrentIndex(2)
        layout = QGridLayout(self.loadPage)
        testBtn = QPushButton('load')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)
   
    def progressFunc(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Text files (*.txt)")
        #positions = parseManifest(filename)
        self.widgetStack.setCurrentIndex(3)
        layout = QGridLayout(self.progressPage)
        testBtn = QPushButton('progress')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)

    def animationFunc(self):
        print("animation")
   
    def contFunc(self):
        self.widgetStack.setCurrentIndex(4)
        layout = QGridLayout(self.animationPage)
        testBtn = QPushButton('test')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)


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
