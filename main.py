from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
import sys

from information_gain import information_gain

import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Integer Calculator")

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.text_inputs = []
        self.result_label = QLabel()

        layout.addWidget(self.result_label)

        # Add +/- buttons for dynamic text input addition/removal
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        add_button = QPushButton("+")
        add_button.clicked.connect(self.add_text_input)
        buttons_layout.addWidget(add_button)

        remove_button = QPushButton("-")
        remove_button.clicked.connect(self.remove_text_input)
        buttons_layout.addWidget(remove_button)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        layout.addWidget(calculate_button)

        self.setCentralWidget(widget)


    def add_text_input(self):
        text_input = QLineEdit()
        text_input.setValidator(QIntValidator())
        self.text_inputs.append(text_input)
        layout = self.centralWidget().layout()
        layout.insertWidget(layout.count() - 2, text_input)

    def remove_text_input(self):
        if self.text_inputs:
            text_input = self.text_inputs.pop()
            layout = self.centralWidget().layout()
            layout.removeWidget(text_input)
            text_input.deleteLater()

    def calculate(self):
        # Perform calculation here
        values = [int(text_input.text()) for text_input in self.text_inputs if text_input.text()]
        result = information_gain(np.array(values))
        self.result_label.setText(f"Information gain: {result}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
