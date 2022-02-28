import os
from sqlite3 import Time
import sys
import random
from datetime import date, datetime
from time import sleep
from typing import List
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QWidget, QPushButton, QVBoxLayout, QFormLayout, QRadioButton, QLineEdit, QCheckBox, QHBoxLayout, QStackedWidget, QListWidget
from PyQt5 import QtCore


def log(description : str, isDev: bool=False):

    subdirectory = "./devlog" if isDev else "./log"
    logfilename = "devlog.txt" if isDev else "log.txt"

    if not os.path.isdir(subdirectory):
        os.makedirs(subdirectory)

    current_date = date.today().strftime("%m/%d/%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    f = open("{0}/{1}".format(subdirectory, logfilename), "a")
    f.write("[{0}] [{1}] {2}\n".format(current_date, current_time, description))
    f.close()
    

def parseManifest(manifest_filename : str) -> List:

    if not os.path.isfile("{0}\{1}".format(os.getcwd(), manifest_filename)):
        log("parseManifest(): Failed to locate {0}\{1}".format(os.getcwd(), manifest_filename), isDev=True)
        return False

    f = open(manifest_filename, 'r')
    containers = [] # e.g. [ (01, 01), 6, "Olive Oil"]
    current_line_number = 0

    for line in f:
        if len(line) < 18: break
        if line[0] != '[': break
        if not line[1:3].isnumeric() or int(line[1:3]) > 8: break
        if line[3] != ',': break
        if not line[4:6].isnumeric() or int(line[1:3]) > 12: break
        if line[6] != ']': break
        if line[7] != ',': break
        if line[8] != ' ': break
        if line[9] != '{': break
        if not line[10:15].isnumeric(): break
        if line[15] != '}': break
        if line[16] != ',': break
        if line[17] != ' ': break

        container_position = ( int(line[1:3]), int(line[4:6]) )
        container_weight = int(line[10:15])
        container_description = line[18:][:-1]

        containers.append([container_position, container_weight, container_description])

        current_line_number += 1

    if current_line_number < 96:
        log("parseManifest(): Error in manifest file on line {0}".format(current_line_number+1), isDev=True)
        return False

    return containers
 
def writeOutboundManifest(containers: List):

    path_to_desktop = "{0}\{1}".format(os.environ['USERPROFILE'], 'Desktop')
    f = open("{0}\{1}".format(path_to_desktop, "manifest_OUTBOUND.txt"), 'w')

    for position, weight, description in containers:

        x = "0{0}".format(position[0]) if len(str(position[0])) == 1 else position[0]
        y = "0{0}".format(position[1]) if len(str(position[1])) == 1 else position[1]
        
        weight = str(weight)

        while len(weight) < 5:
            weight = "0" + weight

        f.write("[{0},{1}], {{{2}}}, {3}\n".format(x, y, weight, description))

    f.close()


class UI(QWidget):

    def __init__(self) -> None:

        super().__init__()

        self.login_page = QWidget()
        self.selection_page = QWidget()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget (self.login_page)
        self.Stack.addWidget (self.selection_page)

        self.login()
        self.selection()

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
        ui.display(ui.selection_page)
        sys.exit(app.exec_())

        



