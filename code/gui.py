from PyQt5.QtGui import *
import sys


def setWindow():
	app = QGuiApplication(sys.argv)
	window = QWindow()
	window.resize(800, 500)
	window.setTitle("Tomograph Simulator")
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	setWindow()
