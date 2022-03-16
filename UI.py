from cgitb import text
from sqlite3 import Time
import sys
from util import *
import grid

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
   QScrollArea,
   QButtonGroup,
   QMessageBox,
   QSizePolicy,
   QInputDialog,
   QPlainTextEdit,
   QListWidget,
   QListWidgetItem,
   QListView,
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
 
app = QApplication(sys.argv)
 
class UI(QWidget):

    #globals to be used by load page
    onloadListNames = []
    onloadListWts = []
    loadRScrollBox = QListWidget()

    #bools! let's not have any memory leaks now
    loginLayoutSet = False
    menuLayoutSet = False
    loadLayoutSet = False
    progressLayoutSet = False
    animationLayoutSet = False
    
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

    def menuConfirmPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure you want to go back to the main menu?")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setEscapeButton(QMessageBox.Cancel)
        if (msg.exec_() == 1024): #1024 = QMessageBox.OK
            #print("Back to menu", flush=True)
            self.menuFunc()
        
    def loginFunc(self):
        self.widgetStack.setCurrentIndex(0)
        if (self.loginLayoutSet == False):

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
            self.loginLayoutSet == True
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(1)
        if (self.menuLayoutSet == False):
            layout = QGridLayout(self.menuPage)

            loginBtn = QPushButton('Login')
            loginBtn.clicked.connect(self.loginFunc)
            balanceBtn = QPushButton('Balance')
            balanceBtn.clicked.connect(self.progressFunc)
            loadBtn = QPushButton('Onload/Offload')
            loadBtn.clicked.connect(self.loadFunc)
            contBtn = QPushButton('Continue')
            contBtn.clicked.connect(self.contFunc)

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
            self.menuLayoutSet == True
        '''
        loginBtn.setStyleSheet("min-height: 5em;")
        balanceBtn.setStyleSheet("min-height: 5em;")
        loadBtn.setStyleSheet("min-height: 5em;")
        contBtn.setStyleSheet("min-height: 5em;")
        '''

    def computeConfirmPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure you want to begin computing the sequence of moves? You will be unable to make any changes when you do.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setEscapeButton(QMessageBox.Cancel)
        if (msg.exec_() == 1024):
            print("BEGINNING COMPUTATION", flush = True)
            #--------------------------------------------------
            #TODO: Pass to AI
            #TODO: To operation-list page
            #--------------------------------------------------

    def addToOnloadList(self):
        cNm, okPressed = QInputDialog.getText(self, "Onload Container", "Enter container contents:")
        if (okPressed):
            cWt, okPressed = QInputDialog.getInt(self, "Onload Container", "Enter container weight:", 0, 0, 5000, 1)
        if (okPressed):
            self.onloadListNames.append(str(cNm))
            self.onloadListWts.append(cWt)
            item = QListWidgetItem()
            item.setText(str(self.onloadListNames.index(cNm) + 1) + ". " + cNm + "   Wt = " + str(cWt))
            self.loadRScrollBox.addItem(item)

    def removeFromOnloadList(self):
            currItem = self.loadRScrollBox.currentItem()
            msg2 = QMessageBox()
            msg2.setWindowTitle("Confirmation")
            msg2.setText("Are you sure you want to remove the following container from the onload list?\n" + currItem.text())
            msg2.setIcon(QMessageBox.Information)
            msg2.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg2.setDefaultButton(QMessageBox.Cancel)
            msg2.setEscapeButton(QMessageBox.Cancel)
            if (msg2.exec_() == 1024):
                ind = int(currItem.text()[0]) - 1
                self.onloadListNames.remove(self.onloadListNames[ind])
                self.onloadListWts.remove(self.onloadListWts[ind])
                gbye = self.loadRScrollBox.takeItem(ind)
                del gbye
                #print("Removed!", flush = True)
                for i in range (0, len(self.onloadListNames)):
                    self.loadRScrollBox.setCurrentRow(i)
                    self.loadRScrollBox.currentItem().setText(str(i+1) + ". " + self.onloadListNames[i] + "   Wt = " + str(self.onloadListWts[i]))
                #print("List refreshed!", flush = True)

    def loadFunc(self):
        #fileName = QFileDialog.getOpenFileName(self, "Open File", os.getenv('HOME'), "Text files (*.txt)")
        #if (fileName != ""):
            #positions = parseManifest(filename)
        #positions = parseManifest(filename)
        self.widgetStack.setCurrentIndex(2)
        if (self.loadLayoutSet == False):
            layout = QHBoxLayout(self.loadPage)
        
            theLeft = QVBoxLayout() #login, back, compute buttons
            theLeft.addWidget(QWidget(), 4)
            loginBtn = QPushButton('Login')
            loginBtn.clicked.connect(self.loginFunc)
            theLeft.addWidget(loginBtn, 1)
            backBtn = QPushButton('Back to Menu')
            backBtn.clicked.connect(self.menuConfirmPopup)
            theLeft.addWidget(backBtn, 1)
            theLeft.addWidget(QWidget(), 3)
            computeBtn = QPushButton('Compute Solution')
            computeBtn.clicked.connect(self.computeConfirmPopup)
            theLeft.addWidget(computeBtn, 1)
            theLeft.addWidget(QWidget(), 10)
        
            theCenter = QVBoxLayout() #grid and title of page
            theCenter.addWidget(QLabel("Unload"), 1, Qt.AlignHCenter)
            theGrid = QGridLayout()
            #Get grid from grid.py
            theCenter.addLayout(theGrid, 18)
            theCenter.addWidget(QWidget(), 1)
        
            theRight = QVBoxLayout() #name and containers to onload
            theRight.addWidget(QLabel("Hello, User!\nNot you? Please log in"), 2)
            addOnlBtn = QPushButton('Add container to onload...')
            addOnlBtn.clicked.connect(self.addToOnloadList)
            theRight.addWidget(addOnlBtn, 4)
            theScrollArea = QScrollArea()
            theScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            theScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            theScrollLayout = QVBoxLayout(theScrollArea)
            theScrollArea.setWidget(theScrollLayout.widget())
            loadList = self.loadRScrollBox
            loadList.itemClicked.connect(self.removeFromOnloadList)
            theScrollLayout.addWidget(loadList)
            loadList.update()
            theRight.addWidget(theScrollArea, 12)
            theRight.addWidget(QWidget(), 2)

            layout.addLayout(theLeft, 1)
            layout.addLayout(theCenter, 5)
            layout.addLayout(theRight, 2)
            layout.setSpacing(10)
 
            self.setLayout(layout)
            self.loadLayoutSet = True
   
    def progressFunc(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", os.getenv('HOME'), "Text files (*.txt)")
        if (fileName != ""):
            #positions = parseManifest(filename)
        self.widgetStack.setCurrentIndex(3)
        if (self.progressLayoutSet == False):
            layout = QGridLayout(self.progressPage)
            testBtn = QPushButton('progress')
            testBtn.clicked.connect(self.loginFunc)
            layout.addWidget(testBtn)
            self.progressLayoutSet == True

    def animationFunc(self):
        if (self.animationLayoutSet == False):
            print("animation", flush = True)
            self.animationLayoutSet == True
   
    def contFunc(self):
        self.widgetStack.setCurrentIndex(4)
        layout = QGridLayout(self.animationPage)
        testBtn = QPushButton('test')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)


if __name__ == "__main__":

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
