import sys

import matplotlib.pyplot as plt
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from pyqtgraph.Qt import QtGui
import numpy as np
import proba

FILENAME = ""
LOADED_PIC_SIZE = 300
RESULT_PIC_SIZE = 620


class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'Tompgraph Simulator'
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

		# self.imageLabel = QLabel(self)
		# px = QPixmap("blank.png")
		# px = px.scaled(LOADED_PIC_SIZE, LOADED_PIC_SIZE, Qt.KeepAspectRatio)
		# self.imageLabel.setPixmap(px)
		# self.imageLabel.setToolTip('The loaded image will appear here.')
		# self.imageLabel.resize(LOADED_PIC_SIZE, LOADED_PIC_SIZE)
		# self.imageLabel.show()

		self.imageView = pg.ImageView(self)
		self.imageView.setToolTip('The loaded image will appear here.')

		param_tree = (
			{'name': 'image_size', 'type': 'int', 'value': 400},
			{'name': 'n_angles', 'type': 'int', 'value': 50},
			{'name': 'n_detectors', 'type': 'int', 'value': 10}
		)
		self.parameters = pg.parametertree.Parameter.create(name='Settings', type='group', children=param_tree)
		self.param_tree = pg.parametertree.ParameterTree()
		self.param_tree.setParameters(self.parameters, showTop=False)
		self.param_tree.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred))
		self.param_tree.setParameters(self.parameters, showTop=False)
		# self.parameters.child('nazwa').value()

		self.startButton = QPushButton('Start', self)
		self.startButton.setToolTip('Click here to start the simulation')
		self.startButton.clicked.connect(self.startClickAction)
		self.startButton.setEnabled(False)

		# self.resultLabel = QLabel(self)
		# px = QPixmap("/code/blank.png")
		# px = px.scaledToWidth(RESULT_PIC_SIZE)
		# self.resultLabel.setPixmap(px)
		# self.resultLabel.setToolTip('The result will appear here.')
		# self.resultLabel.resize(RESULT_PIC_SIZE, RESULT_PIC_SIZE)
		# self.resultLabel.show()

		self.resultView = pg.ImageView(self)
		self.resultView.setToolTip('The result will appear here.')

		self.layout = QtGui.QVBoxLayout(self)
		self.inputLayout = QtGui.QHBoxLayout()

		self.layout.addWidget(self.loadButton)
		self.inputLayout.addWidget(self.param_tree)
		self.inputLayout.addWidget(self.imageView)
		self.layout.addLayout(self.inputLayout)
		self.layout.addWidget(self.startButton)
		self.layout.addWidget(self.resultView)

		self.show()

	@pyqtSlot()
	def loadClickAction(self):
		global FILENAME
		print('load image')
		FILENAME = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)")[0]
		if FILENAME == '': return
		print(FILENAME)

		self.img = plt.imread(FILENAME)
		if len(self.img.shape) == 3:  # RGB
			self.img = self.img[:, :, 0]
		assert len(self.img.shape) == 2
		self.imageView.setImage(self.img, autoLevels=False, levels=(0.01, 1))

		self.startButton.setEnabled(True)

	@pyqtSlot()
	def startClickAction(self):

		n_angles =  self.parameters.child("n_angles").value()
		n_detectors = self.parameters.child("n_detectors").value()
		img_size = self.parameters.child("image_size").value()
		#liczba detektorow: width
		sinogram = np.zeros(shape=(n_angles, n_detectors), dtype=np.int64)
		proba.radon(self.img, sinogram, n_angles, n_detectors,n_detectors)
		print(sinogram)
		new_img = np.zeros(shape=(img_size, img_size), dtype=np.int64)
		proba.reverse_radon(new_img, sinogram, n_detectors, img_size)
		print(new_img)
		self.resultView.setImage(new_img, autoLevels=False, levels=(0.01,1))
		print('start doing stuff')



def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()