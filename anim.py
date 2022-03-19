#!/usr/bin/python

'''
ZetCode Advanced PyQt5 tutorial 
This program animates the size of a
widget with QPropertyAnimation.
Author: Jan Bodnar
Website: zetcode.com 
'''

from concurrent.futures import thread
from email.charset import QP
import multiprocessing
from turtle import update
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QPen, QPalette
from grid import Grid
from util import parseManifest
import sys
import time
from threading import Timer
import threading 
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer, QThreadPool
from multiprocessing import Process
from threading import Thread


def getAnimationFrames(grid : Grid, initialPosition, finalPosition):

    grid.toggleCellSelection(False)

    grids = []

    initialPosition = (8 - initialPosition[0], initialPosition[1]-1)
    finalPosition = (8 - min(8,finalPosition[0]), finalPosition[1]-1)

    currentPosition = [initialPosition[0], initialPosition[1]]
    current_row = currentPosition[0] 
    current_col = currentPosition[1]

    startingCell = grid.item(initialPosition[0], initialPosition[1])
    endingCell = grid.item(finalPosition[0], finalPosition[1])

    startingCell.setBackground( (QColor(235, 67, 61)) )
    endingCell.setBackground( (QColor(43, 194, 63)) )

    
    def colorCellOnGrid(grid: Grid, position, color):
        grid.item(position[0], position[1]).setBackground( color )
        grid.item(1,2).background().color()

    def copyBackgroundColor(grid: Grid, otherGrid: Grid):
        for i in range (0, 8):
            for j in range(0, 12):
                color = QColor(255,255,255) if grid.item(i,j).background().color() == QColor(0,0,0) else grid.item(i,j).background().color()
                otherGrid.item(i, j).setBackground( color ) 

    # colorCellOnGrid(grid, (startingCell[0], startingCell[1]), QColor(235, 67, 61))
    # colorCellOnGrid(grid, (endingCell[0], endingCell[1]), QColor(66, 219, 86))

    if current_row == finalPosition[0]:
        if current_col < finalPosition[1]:
            while current_col < finalPosition[1]:
                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)
                if current_col != initialPosition[1]:
                    colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col += 1
                grids.append(newGrid)
        else:
            while current_col > finalPosition[1]:
                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)
                if current_col != initialPosition[1]:
                    colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col -= 1
                grids.append(newGrid)
    elif current_row > finalPosition[0]:
        while current_row > finalPosition[0]:
            newGrid = Grid(grid.containers)
            newGrid.toggleCellSelection(False)
            copyBackgroundColor(grid if not grids else grids[-1], newGrid)
            if current_row != initialPosition[0]:
                colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
            current_row -= 1
            grids.append(newGrid)
            
        if current_col < finalPosition[1]:
            while current_col < finalPosition[1]:
                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)
                colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col += 1
                grids.append(newGrid)
        else:
            while current_col > finalPosition[1]:
                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)
                colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col -= 1
                grids.append(newGrid)
    elif current_row < finalPosition[0]:

        if current_col < finalPosition[1]:
            while current_col < finalPosition[1]:

                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)

                if current_col != initialPosition[1]:
                    colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col += 1
                grids.append(newGrid)
        else:
            while current_col > finalPosition[1]:
                newGrid = Grid(grid.containers)
                newGrid.toggleCellSelection(False)
                copyBackgroundColor(grid if not grids else grids[-1], newGrid)
                if current_col != initialPosition[1]:
                    colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
                current_col -= 1
                grids.append(newGrid)

        while current_row < finalPosition[0]:
            newGrid = Grid(grid.containers)
            newGrid.toggleCellSelection(False)
            copyBackgroundColor(grid if not grids else grids[-1], newGrid)
            colorCellOnGrid(newGrid, (current_row, current_col), QColor(217, 235, 56))
            current_row += 1
            grids.append(newGrid)


    return grids

def getAnimatedGrid(grid: Grid):
    hbox = QHBoxLayout()
    sw = QStackedWidget()
    frames = getAnimationFrames(grid, (3,3), (7,7))
    for frame in frames: sw.addWidget(frame)

    def changeWidget(widgets):

        while True:
            for i in range(0, len(widgets)):
                sw.setCurrentIndex(i)
                time.sleep(0.10)
                print(2)


    return hbox

class AnimatedGrid(QHBoxLayout):

    def __init__(self, grid, startPos, finalPos):   
        super().__init__()
        self.sw = QStackedWidget()
        self.frames = getAnimationFrames(grid, startPos, finalPos)
        for frame in self.frames:
            self.sw.addWidget(frame)
        self.addWidget(self.sw)

        self.flag = True


        self.x = threading.Thread(target=self.changeWidget, args=())
        self.x.start()
       

    def stop(self):
        self.flag = False


    def changeWidget(self):
        while self.flag:

            for i in range(0, len(self.frames)):
                if self.sw:
                    self.sw.setCurrentIndex(i)
                    time.sleep(0.1)
        return 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QFormLayout()
    grid = Grid(parseManifest("manifest.txt"))
    # frames = [grid] + getAnimationFrames(grid, (2,6), (8,8))


    # hbox = QHBoxLayout()
    # sw = QStackedWidget()

    # for x in frames:
    #     sw.addWidget(x)

    # hbox.addWidget(sw)
    # def xd(widgets):

    #     while True:
    #         for i in range(0, len(widgets)):
    #             sw.setCurrentIndex(i)
    #             time.sleep(0.10)


    # pool = QThreadPool.globalInstance()
    # pool.start(lambda: xd(frames))

    # t = QVBoxLayout()
    # t.addLayout(hbox)

    ag = AnimatedGrid(grid, (1,7), (3,3))
    # ag = AnimatedGrid(grid, (3,4), (7,4))

    window.setLayout(ag)
    window.show()



    sys.exit(app.exec_())