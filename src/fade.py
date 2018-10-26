import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FadeWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self._heightMask = self.height()
        self.animation = QPropertyAnimation(self, b"heightPercentage")
        self.animation.setDuration(1000)
        self.animation.setStartValue(self.height())
        self.animation.setEndValue(-1)
        self.animation.finished.connect(self.close)
        self.isStarted = False

    @pyqtProperty(int)
    def heightMask(self):
        return self._heightMask

    @heightMask.setter
    def heightPercentage(self, value):
        self._heightMask = value
        rect = QRect(0, 0, self.width(), self.heightMask)
        self.setMask(QRegion(rect))

    def closeEvent(self, event):
    	if not self.isStarted:
    		self.animation.start()
    		self.isStarted = True
    		event.ignore()
    	else:
    		QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FadeWidget()
    window.show()
    sys.exit(app.exec_())
