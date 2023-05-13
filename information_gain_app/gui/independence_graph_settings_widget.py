from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class IndependenceGraphSettingsWidget(QWidget):
    nodesUpdated = pyqtSignal(str, str, list)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setWindowTitle("Independence Graph Settings")

        node_layout = QHBoxLayout()
        node_label1 = QLabel('Node 1:')
        self.node1_input = QLineEdit()
        node_layout.addWidget(node_label1)
        node_layout.addWidget(self.node1_input)
        self.node1_input.textChanged.connect(self.emitNodesUpdatedSignal)
        layout.addLayout(node_layout)

        node_layout = QHBoxLayout()
        node_label2 = QLabel("Node 2:")
        self.node2_input = QLineEdit()
        node_layout.addWidget(node_label2)
        node_layout.addWidget(self.node2_input)
        self.node2_input.textChanged.connect(self.emitNodesUpdatedSignal)
        layout.addLayout(node_layout)

        self.given_nodes = []
        given_nodes_label = QLabel("Given Nodes:")
        self.given_nodes_layout = QVBoxLayout()
        self.given_nodes_layout.addWidget(given_nodes_label)

        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.plus_button)
        button_layout.addWidget(self.minus_button)
        layout.addLayout(button_layout)

        self.plus_button.clicked.connect(self.add_given_node)
        self.minus_button.clicked.connect(self.remove_given_node)

        layout.addLayout(self.given_nodes_layout)

    def add_given_node(self):
        given_node_layout = QHBoxLayout()
        given_node_label = QLabel("Given Node:")
        given_node_input = QLineEdit()
        self.given_nodes.append(given_node_input)
        given_node_input.textChanged.connect(self.emitNodesUpdatedSignal)
        given_node_layout.addWidget(given_node_label)
        given_node_layout.addWidget(given_node_input)
        self.given_nodes_layout.addLayout(given_node_layout)

    def remove_given_node(self):
        if len(self.given_nodes) > 0:
            widget = self.given_nodes.pop()
            widget.setParent(None)
            widget.deleteLater()

    def emitNodesUpdatedSignal(self):
        node1 = self.node1_input.text()
        node2 = self.node2_input.text()
        given_nodes = [node.text() for node in self.given_nodes]
        self.nodesUpdated.emit(node1, node2, given_nodes)

    def setup_ui(self):
        pass
