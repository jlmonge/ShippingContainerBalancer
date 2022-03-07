from email.charset import QP
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QPen, QPalette
from util import *
import sys


class Grid(QTableWidget):

    def __init__(self, containers):
        super().__init__()

        self.ROW_SIZE = 8
        self.COL_SIZE = 12
        self.SELECTION_COLOR = QColor(255,228,181)
        self.containers = containers
        self.selectedContainers = set()

        self.setRowCount(self.ROW_SIZE)
        self.setColumnCount(self.COL_SIZE)
        self.setHorizontalHeaderLabels([ str(i).center(15, ' ') for i in range(1, self.COL_SIZE+1)])
        self.setVerticalHeaderLabels([str(i).center(3, ' ') for i in range(self.ROW_SIZE, 0, -1)])
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus) # diasbles border highlighting
        self.setSelectionMode(QAbstractItemView.NoSelection)  # disables widget highlighting https://stackoverflow.com/questions/24973378/how-to-disable-selection-highlighting-in-a-qtablewidget
        self.setEditTriggers(QAbstractItemView.NoEditTriggers) # disables editing of cells
    
        self.horizontalHeader().resizeSections(QHeaderView.ResizeToContents) #width of cell depends on width of header text
        self.setStyleSheet("QTableWidget{border: 1px solid black; width: 200px}")



        self.itemClicked.connect(self.onClick)

        for container in self.containers:
            item = QTableWidgetItem(container[2])

            if container[2] == "NAN":
                item.setBackground(QColor(101, 110, 140))

            self.setItem(self.ROW_SIZE-container[0][0]-1+1, container[0][1]-1, item)


    def onClick(self, item: QTableWidgetItem) -> None:

        row = self.ROW_SIZE-item.row()
        col = item.column()+1

        if item.text() == "NAN": return

        if (row, col) in self.selectedContainers:
            item.setBackground(QColor(255,255,255,0)) #reset background to white
            self.selectedContainers.remove((row, col))
        else:
            item.setBackground(self.SELECTION_COLOR)
            self.selectedContainers.add((row, col))
        
        print(self.getSelectedContainers())
    
    def getSelectedContainers(self) -> List:

        selected = []

        for container in self.containers:
            pos = (container[0][0], container[0][1])
            if pos in self.selectedContainers:
                selected.append(container)
        
        return selected


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QFormLayout()

    layout.addRow(Grid(parseManifest("manifest.txt")))
    window.setLayout(layout)
    window.resize(741, 288)
    window.show()

    sys.exit(app.exec_())

