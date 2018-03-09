import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


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
		self.show()


def startApp():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


if __name__ == '__main__':
	startApp()