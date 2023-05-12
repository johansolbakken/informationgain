from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys

from gui.entropy_gui import EntropyWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Two-Page Application")

    stacked_widget = QStackedWidget()
    window.setCentralWidget(stacked_widget)

    calculator_widget = EntropyWidget()
    stacked_widget.addWidget(calculator_widget)

    window.show()
    sys.exit(app.exec())