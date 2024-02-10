from src.graph import Graph


class Ant:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.path = []
        self.current_node = ""
