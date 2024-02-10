"""
Represents a graph data structure
"""


class Graph:
    def __init__(self):
        # todo: add comments for following varibles
        self.nodes = {}
        self.edges = {}
        self.pheromone_levels = {}
