import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGraphicsView, QFileDialog, \
    QGraphicsScene, QHBoxLayout
from PyQt6.QtCore import Qt

from decision_tree import graphwiz_to_png
from gui.independence_graph_settings_widget import IndependenceGraphSettingsWidget
from independence import IndependenceGraphSpecification, graph_txt_parser, IndependenceGraph, \
    write_moralized_graph_to_graphwiz, write_independence_graph


class IndependenceGraphPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setWindowTitle("Independence Graph Page")

        label = QLabel("This is the Independence Graph page.")
        layout.addWidget(label)

        self.file_chooser = QPushButton("Choose File")
        self.file_chooser.clicked.connect(self.choose_file)
        layout.addWidget(self.file_chooser)

        self.independence_graph_settings = IndependenceGraphSettingsWidget()
        layout.addWidget(self.independence_graph_settings)
        self.independence_graph_settings.nodesUpdated.connect(self.nodesUpdatedSlot)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.calculate_independence_graph)
        layout.addWidget(self.go_button)

        # vbox
        hlayout = QHBoxLayout()
        layout.addLayout(hlayout)

        # Image view for the independence graph
        self.independence_view = QGraphicsView()
        hlayout.addWidget(self.independence_view)

        self.graph_view = QGraphicsView()
        hlayout.addWidget(self.graph_view)

        self.graph_spec = None
        self.node1 = None
        self.node2 = None
        self.given = []

    def nodesUpdatedSlot(self, node1, node2, given):
        self.node1 = node1
        self.node2 = node2
        self.given = given

    def choose_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose File")
        self.graph_spec = graph_txt_parser(file_path)

        graph = IndependenceGraph(self.graph_spec)
        write_independence_graph(graph, "independence_graph.dot")
        graphwiz_to_png("independence_graph.dot")

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("independence_graph.dot.png"))
        self.independence_view.setScene(scene)

        os.remove("independence_graph.dot")
        os.remove("independence_graph.dot.png")

    def calculate_independence_graph(self):
        if self.graph_spec is None:
            return
        if self.node1 is None or self.node2 is None:
            return

        graph = IndependenceGraph(self.graph_spec)
        write_moralized_graph_to_graphwiz(graph, "graph.dot", self.node1, self.node2, self.given)
        graphwiz_to_png("graph.dot")

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("graph.dot.png"))
        self.graph_view.setScene(scene)

        os.remove("graph.dot")
        os.remove("graph.dot.png")
