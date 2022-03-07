import sys
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
   QMessageBox
)
 
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
        self.setWindowIcon(QIcon("icon.png"))
       
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
   
        self.loginFunc()
 
       #start at the login page
 
    def loginFunc(self):
        print("login test")
        self.widgetStack.setCurrentIndex(0)
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        loginBtn = QPushButton('Login')
        layout.addWidget(loginBtn)
 
        loginBtn.clicked.connect(self.menuFunc)
        self.loginPage.setLayout(layout)
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(1)
        layout = QGridLayout()
        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginFunc)
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(self.progressFunc)
        loadBtn = QPushButton('Load/Unload')
        loadBtn.clicked.connect(self.loadFunc)
        contBtn = QPushButton('Continue')
        contBtn.clicked.connect(self.contFunc)
   
        layout.addWidget(loginBtn)
        layout.addWidget(balanceBtn)
        layout.addWidget(loadBtn)
        layout.addWidget(contBtn)
 
        self.menuPage.setLayout(layout)
   
    def loadFunc(self):
        self.widgetStack.setCurrentIndex(2)
        layout = QGridLayout()
        testBtn = QPushButton('load')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)
        self.loadPage.setLayout(layout)
   
    def progressFunc(self):
        self.widgetStack.setCurrentIndex(3)
        layout = QGridLayout()
        testBtn = QPushButton('progress')
        testBtn.clicked.connect(self.loginFunc)
        layout.addWidget(testBtn)
        self.progressPage.setLayout(layout)
   
    def contFunc(self):
        self.widgetStack.setCurrentIndex(4)
        layout = QGridLayout()
        testBtn = QPushButton('test')
        testBtn.clicked.connect(self.loginFunc)



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

'''
class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Keogh's Yard Portage"
        self.width = 1024
        self.height = 576
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet("QWidget {font: 16pt}") # change font size of all widgets
        self.widget = QWidget(self)
        self.grid = QGridLayout()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.grid)
        self.widgets = {
            "login1": [],
            "login2": [],
            "name": [],
            "balance": [],
            "load": [],
            "continue": [],
            "back": [],
            "run": [],
            "unloadText": [],
            "unloadGrid": [],
            "loadText": [],
            "add": [],
            "complete": [],
            "animation": [],
            "instruction": []
        }
        self.loginWidget()

    def clearWidgets(self):
        for w in self.widgets:
            if self.widgets[w] != []:
                self.widgets[w][-1].hide()
            for i in range(0, len(self.widgets[w])):
                self.widgets[w].pop()

    
    def loginWidget(self):
        #self.clearWidgets()
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        #self.setTabText(0,"Contact Details")
    
    def menuWidget(self):
        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginWidget)
        balanceBtn = QPushButton('Balance')
        loadBtn = QPushButton('Onload/Offload')
        contBtn = QPushButton('Continue')

        self.grid.addWidget(loginBtn)
        self.grid.addWidget(balanceBtn)
        self.grid.addWidget(loadBtn)
        self.grid.addWidget(contBtn)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
'''