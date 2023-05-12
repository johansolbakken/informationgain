from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MainPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout(self)
        self.setWindowTitle("Main Page")

        label = QLabel("This is the main page.")
        layout.addWidget(label)

        button = QPushButton("Go to Calculator Page")
        button.clicked.connect(self.go_to_calculator_page)
        layout.addWidget(button)

    def go_to_calculator_page(self):
        self.stacked_widget.setCurrentIndex(1)