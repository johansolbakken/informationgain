import numpy as np

from information_gain_app.decision_tree.information_gain import information_gain


class DecisionTreeSpecification:
    def __init__(self):
        self.attributes = []
        self.data = []


def read_specification(path: str) -> DecisionTreeSpecification:
    specification = DecisionTreeSpecification()
    with open(path, "r") as f:
        line = f.readline()
        line = line.split(",")
        for attr in line:
            specification.attributes.append(attr.strip())

        for line in f.readlines():
            row = line.split(",")
            for i in range(len(row)):
                row[i] = row[i].strip()
            specification.data.append(row)

    return specification


class Node:
    def __init__(self):
        self.children = {}
        self.attribute = None
        self.label = None
        self.value = None


class DecisionTree:
    def __init__(self):
        self.root = None
        self.attributes = []

    def train(self, specification: DecisionTreeSpecification):
        self.attributes = specification.attributes
        self.root = self.build_tree(specification.data, specification.attributes)

    def build_tree(self, data, attributes):
        node = Node()

        if self.all_same_label(data):
            node.label = data[0][-1]
            return node

        if len(attributes) == 0:
            node.label = self.most_common_label(data)
            return node

        node.attribute = self.choose_best_attribute(data, attributes)
        node.value = self.get_values(data, node.attribute)

        for value in node.value:
            sub_data = self.get_data(data, node.attribute, value)
            if len(sub_data) == 0:
                node.label = self.most_common_label(data)
                return node
            else:
                node.children[value] = self.build_tree(sub_data, [x for x in attributes if x != node.attribute])

        return node

    def predict(self, data):
        return self.predict_helper(data, self.root)

    def predict_helper(self, data, node):
        if node.label is not None:
            return node.label
        return self.predict_helper(data, node.children[data[self.attributes.index(node.attribute)]])

    def all_same_label(self, data):
        return len(set([x[-1] for x in data])) == 1

    def most_common_label(self, data):
        labels = [x[-1] for x in data]
        return max(set(labels), key=labels.count)

    def choose_best_attribute(self, data, attributes):
        information_gains = []
        for attribute in attributes:
            # count how many of each value for attribute
            counts = {}
            for x in data:
                counts[x[self.attributes.index(attribute)]] = 0
            for x in data:
                counts[x[self.attributes.index(attribute)]] += 1
            population = np.array(list(counts.values()))
            information_gains.append(information_gain(population))
        return attributes[information_gains.index(max(information_gains))]

    def get_attribute_data(self, data, attribute):
        return [x[self.attributes.index(attribute)] for x in data]

    def get_values(self, data, attribute):
        return list(set(self.get_attribute_data(data, attribute)))

    def get_data(self, data, attribute, value):
        return [
            x
            for x in data
            if x[self.attributes.index(attribute)] == value
        ]


def save_decision_tree_as_graphviz(node: Node, attributes: list, filename: str, title: str = "Decision Tree"):
    with open(filename, "w") as f:
        f.write("digraph G {\n")
        f.write(f"\tgraph [label=\"{title}\", labelloc=t, fontsize=18];\n")
        f.write("\tnode [shape=box];\n")
        f.write("\tedge [fontsize=10];\n")
        f.write("\tgraph [ranksep=0.1];\n")
        f.write("\tgraph [splines=line];\n")
        f.write("\tgraph [fontname=\"Arial\"];\n")
        f.write("\tnode [fontname=\"Arial\"];\n")
        f.write("\tedge [fontname=\"Arial\"];\n")

        save_decision_tree_as_graphviz_helper(node, attributes, f)

        f.write("}")


def save_decision_tree_as_graphviz_helper(node: Node, attributes: list, f):
    if node.label is not None:
        f.write("\t\"{}\" [label=\"{}\"];\n".format(id(node), node.label))
        return

    f.write("\t\"{}\" [label=\"{}\"];\n".format(id(node), node.attribute))
    for value in node.value:
        f.write("\t\"{}\" -> \"{}\" [label=\"{}\"];\n".format(id(node), id(node.children[value]), value))

    for value in node.value:
        save_decision_tree_as_graphviz_helper(node.children[value], attributes, f)


def graphwiz_to_png(filename: str):
    import os
    os.system("dot -Tpng {} -o {}.png".format(filename, filename))


if __name__ == "__main__":
    spec = read_specification("../trees/weather.txt")
    decision_tree = DecisionTree()
    decision_tree.train(spec)
    print("Decision Tree Trained")

    print("Predicting [Rain, Cool, Normal, Strong]")
    print(decision_tree.predict(["Rain", "Cool", "Normal", "Strong"]))
    print("Predicting [Sunny, Hot, High, Weak]")
    print(decision_tree.predict(["Sunny", "Hot", "High", "Weak"]))
    print("Predicting [Overcast, Cool, Normal, Strong]")
    print(decision_tree.predict(["Overcast", "Cool", "Normal", "Strong"]))

    save_decision_tree_as_graphviz(decision_tree.root, decision_tree.attributes, "decision_tree.dot")
    graphwiz_to_png("decision_tree.dot")
