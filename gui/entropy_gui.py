import numpy as np
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout

from information_gain import entropy


class EntropyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entropy Calculator")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        label = QLabel("Entropy Calculator")
        layout.addWidget(label)

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

    def add_text_input(self):
        text_input = QLineEdit()
        text_input.setValidator(QIntValidator())
        self.text_inputs.append(text_input)
        layout = self.layout()
        layout.insertWidget(layout.count() - 2, text_input)

    def remove_text_input(self):
        if self.text_inputs:
            text_input = self.text_inputs.pop()
            layout = self.layout()
            layout.removeWidget(text_input)
            text_input.deleteLater()

    def calculate(self):
        # Perform calculation here
        values = [int(text_input.text()) for text_input in self.text_inputs if text_input.text()]
        result = entropy(np.array(values))
        self.result_label.setText(f"Entropy: {result}")