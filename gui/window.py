from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QToolBar
from PyQt6.QtGui import QAction

from gui.pages import MainPage, DecisionTreePage, CalculatorPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multi-Page Application")
        self.resize(800, 600)

        stacked_widget = QStackedWidget()
        self.setCentralWidget(stacked_widget)

        main_page = MainPage(stacked_widget)
        stacked_widget.addWidget(main_page)

        calculator_widget = CalculatorPage()
        stacked_widget.addWidget(calculator_widget)

        decision_tree_widget = DecisionTreePage()
        stacked_widget.addWidget(decision_tree_widget)

        stacked_widget.setCurrentIndex(0)

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        main_page_action = QAction("Main Page", self)
        main_page_action.triggered.connect(self.go_to_main_page)
        toolbar.addAction(main_page_action)

        calculator_page_action = QAction("Entropy calculator", self)
        calculator_page_action.triggered.connect(self.go_to_calculator_page)
        toolbar.addAction(calculator_page_action)

        decision_tree_page_action = QAction("Decision Tree", self)
        decision_tree_page_action.triggered.connect(self.go_to_decision_tree_page)
        toolbar.addAction(decision_tree_page_action)

    def go_to_main_page(self):
        self.centralWidget().setCurrentIndex(0)

    def go_to_calculator_page(self):
        self.centralWidget().setCurrentIndex(1)

    def go_to_decision_tree_page(self):
        self.centralWidget().setCurrentIndex(2)
