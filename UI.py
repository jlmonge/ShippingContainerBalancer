from cgitb import text
from sqlite3 import Time
import sys
from util import *
import time
from grid import Grid

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

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
   QFileDialog,
   QProgressBar,
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

    #keep him global for use in multiple functions
    loadRScrollBox = QListWidget()

    #bools! let's not reassign stuff
    loginLayoutSet = False
    menuLayoutSet = False
    loadLayoutSet = False
    progressLayoutSet = False
    animationLayoutSet = False
    
    def __init__(self, parent=None):
        super().__init__(parent)
 
        # window config
        self.title = "Keogh's Yard Portage"
        self.width = 1440
        self.height = 880
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
        loginBtn0 = QPushButton('Login', enabled=False)
        layout0.addWidget(loginBtn0)
        loginBtn0.clicked.connect(lambda: self.getName(textfield))
        loginBtn0.clicked.connect(lambda: log(textfield.text() + " has logged in."))

        self.menuPage = QWidget()
        layout1 = QGridLayout(self.menuPage)
        loginBtn1 = QPushButton('Login')
        loginBtn1.clicked.connect(lambda: self.loginFunc(textfield, loginBtn0))
        loadBtn = QPushButton('Onload/Offload')
        loadBtn.clicked.connect(lambda: self.uploadHelper(jobType=0))
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(lambda: self.uploadHelper(jobType=1, progBar=progBar, progBtn=progBtn))
        contBtn = QPushButton('Continue', enabled=False)
        contBtn.clicked.connect(lambda: self.animationFunc(cont=self.cont))
        layout1.addWidget(loginBtn1)
        layout1.addWidget(loadBtn)
        layout1.addWidget(balanceBtn)
        layout1.addWidget(contBtn)

        self.loadPage = QWidget()
        self.loadPage.setMinimumWidth(1300)
        layout2 = QHBoxLayout(self.loadPage)
    

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
                
        unloadLabel = QLabel("Unload")
        # unloadLabel.setStyleSheet("QLabel {background-color: red;}")
        unloadLabel.setFont(QFont('Arial', 30))
        unloadLabel.setMaximumSize(800,50)
        unloadLabel.setAlignment(Qt.AlignCenter)
        theCenter.addWidget(unloadLabel, Qt.AlignCenter)

        grid = Grid(parseManifest("manifest.txt"))
        grid.setMaximumSize(800, 400)
        theCenter.addWidget(grid)

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

        # testBtn = QPushButton('Run')
        # testBtn.clicked.connect(lambda: self.calcFunc(jobType=0, progBar=progBar, progBtn=progBtn))
        # layout2.addWidget(testBtn)   
        # layout2.addWidget(grid)


        layout2.addLayout(theLeft, 1)
        layout2.addLayout(theCenter, 5)
        layout2.addLayout(theRight, 2)
        layout2.setSpacing(10)
 

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

        self.loginFunc(textfield, loginBtn0)
 
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


    def progressFunc(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", os.getenv('HOME'), "Text files (*.txt)")
        containers = parseManifest(fileName[0].rsplit('/', 1)[1])

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
        pass
 
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

    def loginFunc(self, textfield, loginBtn):
        self.widgetStack.setCurrentIndex(0)
        textfield.textChanged[str].connect(lambda: loginBtn.setEnabled(textfield.text() != ""))
        
    
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
