# https://github.com/baoboa/pyqt5/blob/master/examples/widgets/analogclock.py


from PyQt5.QtCore import QPoint, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget


class AnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(2, -2),
        QPoint(-2, -2),
        QPoint(-2, -55),
        QPoint(2, -55)
    ])

    minuteHand = QPolygon([
        QPoint(2, -2),
        QPoint(-2, -2),
        QPoint(-2, -80),
        QPoint(2, -80)
    ])

    secondHand = QPolygon([
        QPoint(1, -1),
        QPoint(-1, -1),
        QPoint(-1, -85),
        QPoint(1, -85)
    ])

    hourColor = QColor(255,250,250)
    minuteColor = QColor(192, 192, 192)
    secondColor = QColor(255, 0, 0)

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.setWindowTitle("Analog Clock")
        self.resize(200, 200)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Hour hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()

        painter.setPen(AnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        # Minute hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()

        painter.setPen(AnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        # Second hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.secondColor)

        painter.save()
        painter.rotate(6.0 * time.second())
        painter.drawConvexPolygon(AnalogClock.secondHand)
        painter.restore()


# if __name__ == '__main__':
#
#     import sys
#
#     app = QApplication(sys.argv)
#     clock = AnalogClock()
#     clock.showFullScreen()
#     sys.exit(app.exec_())
