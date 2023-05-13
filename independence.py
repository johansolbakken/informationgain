import time

from decision_tree import graphwiz_to_png


class Clock:
    def __init__(self):
        # system time
        self.time = time.time() * 1000

    def reset(self):
        self.time = time.time() * 1000

    def get_time(self):
        return time.time() * 1000 - self.time


class IndependenceGraphSpecification:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node: str):
        self.nodes.append(node)

    def add_edge(self, edge: (str, str)):
        self.edges.append(edge)

    def is_edge(self, node1: str, node2: str) -> bool:
        return graph.matrix[self.nodes.index(node1)][self.nodes.index(node2)]


class IndependenceGraph:
    def __init__(self, specification: IndependenceGraphSpecification):
        self.specification = specification
        self.matrix = [[False for _ in range(len(specification.nodes))] for _ in range(len(specification.nodes))]
        for edge in specification.edges:
            self.matrix[specification.nodes.index(edge[0])][specification.nodes.index(edge[1])] = True


def setup_graph(graph: IndependenceGraph, node1: str, node2: str, given: list[str], debug=False) -> IndependenceGraph:
    clock = Clock()

    # Add all nodes in the question
    clock.reset()
    spec = IndependenceGraphSpecification()
    spec.add_node(node1)
    spec.add_node(node2)
    for node in given:
        spec.add_node(node)
    if debug:
        print(f"Add nodes took {clock.get_time()}ms")

    # Add all parents with edges
    clock.reset()
    changed = True
    while changed:
        changed = False
        for node in graph.specification.nodes:
            if node in spec.nodes:
                for parent in graph.specification.nodes:
                    if graph.specification.is_edge(parent, node):
                        if parent not in spec.nodes:
                            spec.add_node(parent)
                            changed = True
                        if (parent, node) not in spec.edges:
                            spec.add_edge((parent, node))
                            changed = True
    if debug:
        print(f"Add parents took {clock.get_time()}ms")

    # Make graph
    clock.reset()
    new_graph = IndependenceGraph(spec)
    if debug:
        print(f"Make graph took {clock.get_time()}ms")

    # Moralizing
    clock.reset()
    for i in range(len(spec.nodes)):
        for j in range(len(spec.nodes)):
            if i != j:
                common_child = False
                for k in range(len(spec.nodes)):
                    if new_graph.matrix[i][k] and new_graph.matrix[j][k]:
                        common_child = True
                        break
                if common_child:
                    new_graph.matrix[i][j] = True
                    new_graph.matrix[j][i] = True
    if debug:
        print(f"Moralizing took {clock.get_time()}ms")

    # Make unidirected
    clock.reset()
    for i in range(len(spec.nodes)):
        for j in range(len(spec.nodes)):
            if new_graph.matrix[i][j] or new_graph.matrix[j][i]:
                new_graph.matrix[i][j] = True
                new_graph.matrix[j][i] = True
    if debug:
        print(f"Make unidirected took {clock.get_time()}ms")

    return new_graph


def is_independent(graph: IndependenceGraph, node1: str, node2: str, given: list[str], debug=False) -> bool:
    clock = Clock()
    algoClock = Clock()
    new_graph = setup_graph(graph, node1, node2, given, debug)

    # check if there is a path from node1 to node2 that does not go through any node in given
    clock.reset()
    visited = [False for _ in range(len(new_graph.specification.nodes))]
    queue = [node1]
    independence = True
    while len(queue) > 0:
        node = queue.pop(0)
        if node == node2:
            independence = False
            break
        visited[new_graph.specification.nodes.index(node)] = True
        for i in range(len(new_graph.specification.nodes)):
            if new_graph.matrix[new_graph.specification.nodes.index(node)][i] and not visited[i] and \
                    new_graph.specification.nodes[i] not in given:
                queue.append(new_graph.specification.nodes[i])
    if debug:
        print(f"Check path took {clock.get_time()}ms")

    if debug:
        print(f"Total time: {algoClock.get_time()}ms")

    return independence


def write_independence_graph(graph: IndependenceGraph, filename: str):
    graphwiz = "digraph {\n"
    for i in range(len(graph.specification.nodes)):
        graphwiz += f"\t{graph.specification.nodes[i]}\n"
    for i in range(len(graph.specification.nodes)):
        for j in range(len(graph.specification.nodes)):
            if graph.matrix[i][j]:
                graphwiz += f"\t{graph.specification.nodes[i]} -> {graph.specification.nodes[j]}\n"
    graphwiz += "}"
    with open(filename, "w") as file:
        file.write(graphwiz)


def write_moralized_graph_to_graphwiz(graph: IndependenceGraph, filename: str, node1: str, node2: str,
                                      given: list[str]):
    new_graph = setup_graph(graph, node1, node2, given)
    independence = is_independent(graph, node1, node2, given)
    graphwiz = "graph {\n"
    graphwiz += f"\tlabel=\"{node1} and {node2} are {'independent' if independence else 'dependent'} given {given}\"\n"
    for i in range(len(new_graph.specification.nodes)):
        if new_graph.specification.nodes[i] in given:
            graphwiz += f"\t{new_graph.specification.nodes[i]} [penwidth=3]\n"
        if new_graph.specification.nodes[i] == node1 or new_graph.specification.nodes[i] == node2:
            graphwiz += f"\t{new_graph.specification.nodes[i]} [style=filled, fillcolor=lightgrey,penwidth=3]\n"
        graphwiz += f"\t{new_graph.specification.nodes[i]}\n"
    drawn_edges = []
    for i in range(len(new_graph.specification.nodes)):
        for j in range(len(new_graph.specification.nodes)):
            if new_graph.matrix[i][j] and ((i, j) not in drawn_edges) and ((j, i) not in drawn_edges):
                graphwiz += f"\t{new_graph.specification.nodes[i]} -- {new_graph.specification.nodes[j]}\n"
                drawn_edges.append((i, j))
    graphwiz += "}"
    with open(filename, "w") as file:
        file.write(graphwiz)


if __name__ == "__main__":
    specification = IndependenceGraphSpecification()
    specification.add_node("A")
    specification.add_node("B")
    specification.add_node("C")
    specification.add_node("D")
    specification.add_node("E")
    specification.add_node("F")
    specification.add_node("G")
    specification.add_node("H")
    specification.add_node("I")
    specification.add_node("J")

    specification.add_edge(("A", "D"))
    specification.add_edge(("A", "E"))
    specification.add_edge(("B", "E"))
    specification.add_edge(("B", "F"))
    specification.add_edge(("C", "F"))
    specification.add_edge(("C", "G"))
    specification.add_edge(("D", "I"))
    specification.add_edge(("E", "H"))
    specification.add_edge(("H", "I"))
    specification.add_edge(("H", "J"))

    graph = IndependenceGraph(specification)
    print(is_independent(graph, "I", "G", ["F", "H", "D"], debug=True))
    write_moralized_graph_to_graphwiz(graph, "graph.dot", "I", "G", ["F", "H", "D"])
    write_independence_graph(graph, "independence_graph.dot")
    graphwiz_to_png("graph.dot")
    graphwiz_to_png("independence_graph.dot")
