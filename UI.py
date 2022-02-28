import os
import sys
from datetime import date, datetime
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
        



