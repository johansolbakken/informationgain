from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsView, QFileDialog, QGraphicsScene

from information_gain_app.decision_tree import decision_tree_graphwiz
from information_gain_app.decision_tree.decision_tree import read_specification, DecisionTree, \
    graphwiz_to_png

import os

from information_gain_app.decision_tree.decision_tree_graphwiz import save_decision_tree_as_graphviz

"""
TODO: I think that the decision tree does not consider multiple attributes. For example, if the specification is:
    outlook: sunny, overcast, rainy
    temperature: hot, mild, cool
    humidity: high, normal
    windy: true, false
    play: yes, no
Then the decision tree should consider all of the attributes, not just one. For example, the decision tree should
Currently it only has two attributes per node. It should have all of the attributes per node.
"""


class DecisionTreePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setWindowTitle("Decision Tree Page")

        label = QLabel("This is the decision tree page.")
        layout.addWidget(label)

        self.file_chooser = QPushButton("Choose Description File")
        self.file_chooser.clicked.connect(self.choose_file)
        layout.addWidget(self.file_chooser)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.start_decision_tree)
        layout.addWidget(self.go_button)

        self.image_view = QGraphicsView()
        layout.addWidget(self.image_view)

        self.decision_tree_specification_file = ""

    def choose_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose Description File")
        self.decision_tree_specification_file = file_path

    def start_decision_tree(self):
        if self.decision_tree_specification_file == "":
            return
        specification = read_specification(self.decision_tree_specification_file)
        decision_tree = DecisionTree()
        decision_tree.train(specification)

        decision_tree_graphwiz.save_decision_tree_as_graphviz(decision_tree.root, decision_tree.attributes,
                                                              "decision_tree.dot",
                                                              self.decision_tree_specification_file.split(".")[0].split(
                                                                  "/")[
                                                                  len(self.decision_tree_specification_file.split(".")[
                                                                          0].split("/")) - 1])
        graphwiz_to_png("decision_tree.dot")
        os.remove("decision_tree.dot")

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("decision_tree.dot.png"))
        self.image_view.setScene(scene)

        os.remove("decision_tree.dot.png")
