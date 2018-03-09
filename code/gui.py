import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot


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
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		loadButton = QPushButton('Load image', self)
		loadButton.setToolTip('Click here to load the image from files')
		loadButton.resize(100, 100)
		loadButton.move(10, 10)
		loadButton.clicked.connect(self.loadClickAction)

		self.show()

	@pyqtSlot()
	def loadClickAction(self):
		print('load image')
		fileName = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)")[0]
		if fileName == '': return
		print(fileName)
		self.startImage = plt.imread(fileName)
		if len(self.startImage.shape) == 3:  # RGB
			self.startImage = self.startImage[:, :, 0]
		assert len(self.startImage.shape) == 2


def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()
