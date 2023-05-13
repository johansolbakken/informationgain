from information_gain_app.decision_tree import decision_tree


def save_tree(node: decision_tree.Node, attributes: list, filename: str, title: str = "Decision Tree"):
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
        save_tree_helper(node, attributes, f)
        f.write("}")


def save_tree_helper(node: decision_tree.Node, attributes: list, f):
    if node.label is not None:
        f.write("\t\"{}\" [label=\"{}\"];\n".format(id(node), node.label))
        return

    f.write("\t\"{}\" [label=\"{}\"];\n".format(id(node), node.attribute))
    for value in node.value:
        f.write("\t\"{}\" -> \"{}\" [label=\"{}\"];\n".format(id(node), id(node.children[value]), value))

    for value in node.value:
        save_tree_helper(node.children[value], attributes, f)
