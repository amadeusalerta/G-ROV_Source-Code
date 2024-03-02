import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initialize variables to track key presses
        self.keyPressed = False
        self.lastKey = ''

        # Set up a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.processKeyPress)
        self.timer.start(50)  # Set the interval to 1000 milliseconds (1 second)

    def initUI(self):
        self.label = QLabel("Wait for key press", self)
        self.setGeometry(300, 300, 280, 150)
        self.setWindowTitle('Keyboard Interval Example')
        self.show()

    def keyPressEvent(self, event):
        # Mark that a key was pressed and store the last key
        self.keyPressed = True
        self.lastKey = event.text()

    def processKeyPress(self):
        # Process the key press event here
        if self.keyPressed:
            self.label.setText(f"Last Key: {self.lastKey}")
            # Reset the keyPressed flag
            self.keyPressed = False
        else:
            self.label.setText("No key press detected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
