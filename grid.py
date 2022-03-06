from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from util import *


class Grid(QTableWidget):

    def __init__(self):
        super().__init__()

        ROW_SIZE = 8
        COL_SIZE = 12

        containers = parseManifest("manifest.txt")

        self.setRowCount(ROW_SIZE)
        self.setColumnCount(COL_SIZE)
        self.setHorizontalHeaderLabels([str(i) for i in range(1, COL_SIZE+1)])
        self.setVerticalHeaderLabels([str(i) for i in range(ROW_SIZE, 0, -1)])

        for container in containers:
            item = QTableWidgetItem(container[2])

            self.setItem(ROW_SIZE-container[0][0]-1+1, container[0][1]-1, item)

       
    def onCellSelection(row: int, col: int):
        print(row, col)
            