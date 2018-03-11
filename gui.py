import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np


def line_coord(alpha: float, disp: float, size: int):
    r_circle = size // 2
    max_r = int(np.sqrt((r_circle ** 2) - (disp ** 2))) - 1
    span_r = range(-max_r, max_r)
    sin_a = np.sin(alpha)
    cos_a = np.cos(alpha)
    dx = -int(disp * sin_a)
    dy = int(disp * cos_a)
	
    matrix = []
	
    for r in span_r:
        rx = r_circle + int(r*cos_a) + dx
        ry = r_circle + int(r*sin_a) + dy
        matrix.append((rx,ry))		
	
    return matrix


def draw_line(img, size, alpha, delta, value):
    matrix = line_coord(alpha, delta, size)
    for (x,y) in matrix:
        img[x,y] = value		


def draw_rays(img_size: int, n_angles: int, n_detectors: int, width: float) -> np.ndarray:
    img = np.zeros((img_size, img_size), dtype=float)

    width_det_line = img_size * width
    for ang in range(n_angles):
        for detector in range(n_detectors):
            angle = ang/n_angles * np.pi
            delta = width_det_line * (-0.5 + detector/n_detectors)
            value = (ang+1)/n_angles
            draw_line(img, img_size, angle, delta, value)
    return img


def test():
    img_size = 400
    n_angles = 20
    n_detectors = 20
    width = 0.4
    img = draw_rays(img_size, n_angles, n_detectors, width)
    return img
    

FILENAME = ""
LOADED_PIC_SIZE = 300
RESULT_PIC_SIZE = 620


class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'Tomograph Simulator'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		global LOADED_PIC_SIZE, RESULT_PIC_SIZE
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.loadButton = QPushButton('Load image', self)
		self.loadButton.setToolTip('Click here to load the image from files')
		self.loadButton.clicked.connect(self.loadClickAction)

		self.imageLabel = QLabel(self)
		px = QPixmap("blank.png")
		px = px.scaled(LOADED_PIC_SIZE, LOADED_PIC_SIZE, Qt.KeepAspectRatio)
		self.imageLabel.setPixmap(px)
		self.imageLabel.setToolTip('The loaded image will appear here.')
		self.imageLabel.resize(LOADED_PIC_SIZE, LOADED_PIC_SIZE)
		self.imageLabel.show()

		param_tree = (
			{'name': 'img_size', 'type': 'int', 'value': 400},
			{'name': 'n_angles', 'type': 'int', 'value': 50},
			{'name': 'n_detectors', 'type': 'int', 'value': 10},
			{'name': 'width', 'type': 'float', 'value': 0.9},
			{'name': 'mask_size', 'type': 'float', 'value': 5},
			{'name': 'play_rate', 'type': 'int', 'value': 2}
		)
		self.parameters = pg.parametertree.Parameter.create(name='Settings', type='group', children=param_tree)
		self.param_tree = pg.parametertree.ParameterTree()
		self.param_tree.setParameters(self.parameters, showTop=False)
		self.param_tree.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred))

		self.startButton = QPushButton('Start', self)
		self.startButton.setToolTip('Click here to start the simulation')
		self.startButton.clicked.connect(self.startClickAction)
		self.startButton.setEnabled(False)

		self.resultLabel = QLabel(self)
		px = QPixmap("blank.png")
		px = px.scaledToWidth(RESULT_PIC_SIZE)
		self.resultLabel.setPixmap(px)
		self.resultLabel.setToolTip('The result will appear here.')
		self.resultLabel.resize(RESULT_PIC_SIZE, RESULT_PIC_SIZE)
		self.resultLabel.show()

		self.layout = QtGui.QVBoxLayout(self)
		self.inputLayout = QtGui.QHBoxLayout()

		self.layout.addWidget(self.loadButton)
		self.inputLayout.addWidget(self.param_tree)
		self.inputLayout.addWidget(self.imageLabel)
		self.layout.addLayout(self.inputLayout)
		self.layout.addWidget(self.startButton)
		self.layout.addWidget(self.resultLabel)

		self.show()

	@pyqtSlot()
	def loadClickAction(self):
		global FILENAME
		print('load image')
		FILENAME = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)")[0]
		if FILENAME == '': return
		print(FILENAME)

		px = QPixmap(FILENAME)
		px = px.scaled(LOADED_PIC_SIZE, LOADED_PIC_SIZE, Qt.KeepAspectRatio)

		self.imageLabel.setPixmap(px)
		self.imageLabel.setToolTip(FILENAME)
		self.imageLabel.resize(LOADED_PIC_SIZE, LOADED_PIC_SIZE)
		self.imageLabel.show()

		self.startButton.setEnabled(True)

	@pyqtSlot()
	def startClickAction(self):
		img = test()
		img = QtGui.QImage(img, img.shape[1],img.shape[0], img.shape[1] * 3,QtGui.QImage.Format_RGB888)
		pix = QPixmap(img)

		pix = pix.scaled(LOADED_PIC_SIZE, LOADED_PIC_SIZE, Qt.KeepAspectRatio)

		self.imageLabel.setPixmap(pix)
		self.imageLabel.show()



def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
    startApp()