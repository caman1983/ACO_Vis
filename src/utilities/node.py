class Node:
    def __init__(self, node_id: str):
        # todo: add comments here
        self.id = node_id
        self.coordinates = (0, 0)

    def set_coordinates(self, x: int, y: int):
        self.coordinates = (x, y)

