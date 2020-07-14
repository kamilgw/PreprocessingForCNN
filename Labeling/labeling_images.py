import os
import re
import time
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter, QCursor
import cv2
import numpy as np
from PyQt5.QtWidgets import *

WINDOW_NAME = 'Labeling images'

class_index = 0
img_index = 0
img = None

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap('D:/Wagony/zdjWag/00000.png'))

        self.setCursor(QCursor(Qt.CrossCursor))
        self.bounding_boxes = []
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)
        for points in self.bounding_boxes:
            qp.drawRect(QtCore.QRect(*points))
        qp.drawRect(QtCore.QRect(self.begin, self.end))
        self.update()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        if not self.begin.isNull():
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.bounding_boxes.append([self.begin, self.end])
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()



class QPaletteButton(QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Preprocessing images")
        self.canvas = Canvas()
        self.button_img_folder = QPushButton("Choose folder")
        self.button_img_folder.clicked.connect(self.get_image_file)

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.button_img_folder)
        l.addWidget(self.canvas)


        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)


        # palette = QtWidgets.QHBoxLayout()
        # l.addLayout(palette)

        self.setCentralWidget(w)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def get_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self,"Open Image Folder","D:\\Wagony\\zdjWag\\")
        print(file_name)
        self.canvas.setPixmap(QPixmap(file_name))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

class BoundingBox:
    pass


def set_class_index(index):
    global class_index
    class_index = index
    description = f'Your class index is {class_index}'
    print(description)


def set_img_index(index):
    global img_index
    img_index = index
    description = f'Your image index is {img_index}'
    print(description)


def previous_index(index, last_index):
    index -= 1
    if index < 0:
        index = last_index
    return index


def next_index(index, last_index):
    index += 1
    if index > last_index:
        index = 0
    return index

# cv2.namedWindow(WINDOW_NAME)
# cv2.resizeWindow(WINDOW_NAME, 1280, 800)
# time.sleep(2)
