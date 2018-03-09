import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt

FILENAME = ""


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

		self.loadButton = QPushButton('Load image', self)
		self.loadButton.setToolTip('Click here to load the image from files')
		# self.loadButton.resize(100, 100)
		self.loadButton.move(10, 10)
		self.loadButton.clicked.connect(self.loadClickAction)

		self.imageLabel = QLabel(self)

		self.show()

	@pyqtSlot()
	def loadClickAction(self):
		global FILENAME
		print('load image')
		FILENAME = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)")[0]
		if FILENAME == '': return
		print(FILENAME)

		px = QPixmap(FILENAME)
		px = px.scaled(200, 200, Qt.KeepAspectRatio)

		self.imageLabel.setPixmap(px)
		self.imageLabel.setToolTip(FILENAME)
		self.imageLabel.move(10, self.loadButton.height()+20)
		self.imageLabel.resize(200, 200)
		self.imageLabel.show()



def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()
