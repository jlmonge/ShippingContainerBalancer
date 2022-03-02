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
    QStackedLayout
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



class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Keogh's Yard Portage"
        self.width = 1024
        self.height = 576
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("icon.png"))
        self.widget = QWidget(self)
        self.grid = QGridLayout()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.grid)
        '''
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
        '''
        self.menuWidget()

    '''
    def clearWidgets(self):
        for w in self.widgets:
            if self.widgets[w] != []:
                self.widgets[w][-1].hide()
            for i in range(0, len(self.widgets[w])):
                self.widgets[w].pop()
    '''

    
    def loginWidget(self):
        #self.clearWidgets()
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        #self.setTabText(0,"Contact Details")
        return 
    
    def menuWidget(self):
        loginBtn = QPushButton('Login')
        loginBtn.clicked.connect(self.loginWidget)
        balanceBtn = QPushButton('Balance')
        loadBtn = QPushButton('Load/Unload')
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