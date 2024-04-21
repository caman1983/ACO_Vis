from typing import List
from src.entities.ant import Ant
from src.graph_components.graph import Graph


#
class AntManager:
    def __init__(self, graph: Graph, num_ants: int, start_node) -> None:
        self.graph = graph
        self.ants: List[Ant] = [Ant(graph, start_node) for _ in range(num_ants)]