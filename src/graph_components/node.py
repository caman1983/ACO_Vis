class Node:
    """
    Represents a node in a graph, identified by an ID and associated with specific coordinates.
    """

    def __init__(self, node_id: str):
        """
        Initialises a new instance of the Node class.

        :param node_id: A unique identifier for the node.
        """
        self.id = node_id
        self.coordinates = (0, 0)  # Default coordinates (x=0, y=0)

    def set_coordinates(self, x: float, y: float) -> None:
        """
        Sets the coordinates of the node.

        :param x: The x-coordinate of the node.
        :param y: The y-coordinate of the node.
        """
        self.coordinates = (x, y)

    def __repr__(self) -> str:
        """
        Returns a representation of the node, showing its ID and coordinates.
        """
        return f"Node(id={self.id}, coordinates={self.coordinates})"