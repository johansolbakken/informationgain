from PyQt6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget, QRadioButton, QButtonGroup

from information_gain_app.gui.entropy_gui import EntropyWidget
from information_gain_app.gui.information_gain_gui import InformationGainWidget


class CalculatorPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setWindowTitle("Calculator Page")

        label = QLabel("This is the calculator page.")
        layout.addWidget(label)

        self.button_group = QButtonGroup()
        self.button_group.buttonClicked.connect(self.on_button_clicked)

        entropy_button = QRadioButton("Entropy Mode")
        self.button_group.addButton(entropy_button)
        layout.addWidget(entropy_button)

        information_gain_button = QRadioButton("Information Gain Mode")
        self.button_group.addButton(information_gain_button)
        layout.addWidget(information_gain_button)

        entropy_button.setChecked(True)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        entropy_widget = EntropyWidget()
        self.stacked_widget.addWidget(entropy_widget)

        information_gain_widget = InformationGainWidget()
        self.stacked_widget.addWidget(information_gain_widget)

        self.stacked_widget.setCurrentIndex(0)

    def on_button_clicked(self, button):
        if button.text() == "Entropy Mode":
            self.stacked_widget.setCurrentIndex(0)
        elif button.text() == "Information Gain Mode":
            self.stacked_widget.setCurrentIndex(1)

    def go_to_entropy_mode(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_information_gain_mode(self):
        self.stacked_widget.setCurrentIndex(1)
