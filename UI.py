import os
import sys
from datetime import date, datetime
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget



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

        window = QWidget()
        window.setWindowTitle("Keogh's Yard Portage")
        window.setGeometry(100, 100, 1600, 900)
        window.move(60, 15)
        helloMsg = QLabel('Login', parent=window)

        window.show()
        sys.exit(app.exec_())
        



