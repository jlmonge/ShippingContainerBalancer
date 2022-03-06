from sqlite3 import Time
import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QWidget, QPushButton, QTableWidgetItem, QFormLayout, QRadioButton, QLineEdit, QCheckBox, QHBoxLayout, QStackedWidget, QTableWidget, QTableView 
from grid import Grid
from util import *



class UI(QWidget):

    def __init__(self) -> None:

        super().__init__()

        self.login_page = QWidget()
        self.selection_page = QWidget()
        self.grid_page = QWidget()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget (self.login_page)
        self.Stack.addWidget (self.selection_page)
        self.Stack.addWidget (self.grid_page)

        self.login()
        self.selection()
        self.grid()

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.setGeometry(300, 50, 10,10)
        self.setWindowTitle('Team B')
        self.show()

    def login(self):
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        #self.setTabText(0,"Contact Details")
        self.login_page.setLayout(layout)
            
    def selection(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())
            
        self.selection_page.setLayout(layout)

    def grid(self):

        layout = QFormLayout()
        sex = QHBoxLayout()

        tableWidget = Grid()


        sex.addWidget(tableWidget)
        layout.addRow(sex)
        self.grid_page.setLayout(layout)
            

    def display(self, widget : QWidget):
        self.Stack.setCurrentWidget(widget)




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
        ui.resize(800, 600)
        ui.display(ui.grid_page)
        sys.exit(app.exec_())

        



