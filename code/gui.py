import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
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


def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()
