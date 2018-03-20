import sys

import matplotlib.pyplot as plt
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from pyqtgraph.Qt import QtGui
import numpy as np
import logic
from PIL import Image

FILENAME = ""
LOADED_PIC_SIZE = 300
RESULT_PIC_SIZE = 300
result_img = ""


PLAY_RATE = 5

class App(QWidget):

	def __init__(self):
		QWidget.__init__(self)
		self.title = 'Tomograph Simulator'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		
		#self.layout.addWidget(self.progress_bar)
		self.initUI()

	def initUI(self):
		global LOADED_PIC_SIZE, RESULT_PIC_SIZE
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.loadButton = QPushButton('Load image', self)
		self.loadButton.setToolTip('Click here to load the image from files')
		self.loadButton.clicked.connect(self.loadClickAction)

		self.imageView = pg.ImageView(self)
		self.imageView.setToolTip('The loaded image will appear here.')

		param_tree = (
			{'name': 'image_size', 'type': 'int', 'value': 400},
			{'name': 'n_angles', 'type': 'int', 'value': 50},
			{'name': 'n_detectors', 'type': 'int', 'value': 10},
            {'name': 'width', 'type': 'float', 'value': 0.9},
            {'name': 'mask_size', 'type': 'float', 'value': 5}
		)
		self.parameters = pg.parametertree.Parameter.create(name='Settings', type='group', children=param_tree)
		self.param_tree = pg.parametertree.ParameterTree()
		self.param_tree.setParameters(self.parameters, showTop=False)
		self.param_tree.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred))

		self.startButton = QPushButton('Start', self)
		self.startButton.setToolTip('Click here to start the simulation')
		self.startButton.clicked.connect(self.startClickAction)
		self.startButton.setEnabled(False)

		self.saveButton = QPushButton('Save image', self)
		self.saveButton.setToolTip('Click here to save the output image')
		self.saveButton.clicked.connect(self.saveAction)
		self.saveButton.setEnabled(False)

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
		self.layout.addWidget(self.saveButton)

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
		global result_img
		self.startButton.setEnabled(False)
		width = self.parameters.child('width').value()
		n_angles = self.parameters.child('n_angles').value()
		n_detectors = self.parameters.child('n_detectors').value()
		
		sinogram = np.zeros(shape=(n_angles, n_detectors), dtype=np.int64)

		logic.radon(self.img, sinogram, n_angles, n_detectors, width)
		mask_size = self.parameters.child('mask_size').value()
		if mask_size > 0  and mask_size < 6:
			mask = logic.get_mask(mask_size)
			print("Mask: {}".format(mask))
			sinogram = logic.filter(sinogram, mask)

		img_size = self.parameters.child('image_size').value()
		result_img = np.zeros(shape=(n_angles, img_size, img_size), dtype=np.float64)

		logic.reverse_radon(result_img, sinogram, width, img_size)
		test_slice = result_img[-1, img_size//2, :]
		min_value = np.percentile(test_slice, 5.0)
		max_value = np.percentile(test_slice, 95.0)
		print("Levels: ({}, {})".format(min_value, max_value))
		self.resultView.setImage(result_img, autoLevels=False,
                                  levels=(min_value, max_value))
		self.resultView.play(PLAY_RATE)
		self.startButton.setEnabled(True)
		self.saveButton.setEnabled(True)

	@pyqtSlot()
	def	saveAction(self):
		global result_img
		im = Image.fromarray(result_img)
		im.save("your_file.jpeg")



def startApp():
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(800, 500)
	ex.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()