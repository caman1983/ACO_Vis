import random
from src.graph_components.graph import Graph


class Ant:
    def __init__(self, graph: Graph, start_node: str) -> None:
        self.graph = graph
        self.path = [start_node]  # list to record path taken by ant
        self.STARTING_NODE_ID = start_node  # constant, a record of the home node

        # for movement
        self.__current_node = start_node  # the ants current node on the graph
        self.__previous_node = None  # Track the previous node to avoid immediate backtracking
        self.__current_position = self.graph.get_node_coordinates(start_node)  # current x,y coordinate values of ant
        self.__target_node_id = None  # initialise as none as a target has not been selected yet
        self.__speed = 15

    def move_toward_target(self):
        """
        Moves the ant towards its target node, updating its position and state.
        """
        # get xy coordinates of target node
        target_node_coordinates = self.graph.get_node_coordinates(self.__target_node_id)

        # calculate horizontal difference between ants position and target node
        dx = target_node_coordinates[0] - self.__current_position[0]
        # calculate vertical difference between ants position and target node
        dy = target_node_coordinates[1] - self.__current_position[1]
        # calculate distance to target
        distance = (dx ** 2 + dy ** 2) ** 0.5

        threshold = max(self.__speed, 5)  # Use speed or a minimum value, e.g., 5 pixels
        if distance > threshold:
            dx /= distance
            dy /= distance
            self.__current_position = (
                self.__current_position[0] + dx * self.__speed,
                self.__current_position[1] + dy * self.__speed,
            )

        else:
            # if ant has reached target node, update ant state

            # Update the previous node before changing the current node
            self.__previous_node = self.__current_node

            # set current position (coordinates) to target node, as target node is reached
            self.__current_position = target_node_coordinates

            # set current node to target node, as target node has been reached
            self.__current_node = self.__target_node_id

            self.__target_node_id = None  # Reset target node to allow selection of a new target

    def get_probabilities(self, alpha, beta) -> list[tuple[str, float]]:
        """
        Calculate the probabilities of moving from the current node to each connected node based on the
        pheromone levels and the distances to these nodes.

        Parameters:
        - alpha (float): The exponent to control the influence of the pheromone level.
        - beta (float): The exponent to control the influence of the inverse of the distance (desirability).

        Returns:
        - list[tuple[str, float]]: A list of tuples, each containing a node identifier and its corresponding
          normalized probability of being selected as the next node.
        """
        # get list of connected nodes to current node, excluding current and previous node
        connected_nodes = self.graph.get_connected_nodes(self.__current_node, self.__previous_node)
        probabilities = []
        total = 0
        # iterate through list of traversal nodes
        for node in connected_nodes:
            # get pheromone level between current node and potential next node
            pheromone_level = self.graph.get_pheromone_level((self.__current_node, node))
            # get distance metric between current node and potential next node
            distance = self.graph.get_distance((self.__current_node, node))
            # calculate desirability based on distance
            desirability = 1 / distance

            if distance <= 0:
                raise Exception("Critical error: Distance between nodes cannot be less then zero")

            node_potential = (pheromone_level ** alpha) * (desirability ** beta)
            probabilities.append((node, node_potential))
            # summation of all node probabilities
            total += node_potential

        normalised_probabilities = [(node_id, round(probability / total, 2)) for node_id, probability in probabilities]
        return normalised_probabilities

    # determines and returns next node based on probabilities calculated
    def get_next_node(self, probabilities: list[tuple[str, float]]) -> str:
        """
        Determines the next node based on the calculated probabilities. If the list of probabilities is empty,
        performs backtracking to the previous node.

        Parameters:
        - probabilities (list[tuple[str, float]]): A list of tuples containing node identifiers and their
          corresponding selection probabilities.

        Returns:
        - str: The identifier of the next node or the node to backtrack to if no forward path is available.
        """
        if probabilities:
            node_id, probability = zip(*probabilities)
            next_node = random.choices(node_id, weights=probability, k=1)[0]

            self.path.append(next_node)  # add ants next node to path
            return next_node

        # if probabilities list is empty (ant has no traversable path to go) return to previous node
        elif not probabilities:
            if len(self.path) > 1:
                self.path.pop()  # Remove current node from path
                backtrack_node = self.path[-1]
                self.set_target_node(backtrack_node)
                return self.__target_node_id

    def get_path_length(self):
        """
        Calculates the total length of the path traversed by summing the distances between consecutive nodes.

        Returns:
        - float: The total length of the path.
        """
        total_length = 0
        for i in range(len(self.path) - 1):
            # get distance between current node element and next node element
            edge_length = self.graph.get_distance((self.path[i], self.path[i + 1]))
            total_length += edge_length

        return total_length

    def has_target_node(self) -> bool:
        if self.__target_node_id is not None:
            return True
        else:
            return False

    def set_target_node(self, target_node_id: str):
        self.__target_node_id = target_node_id

    def set_current_node(self, node_id: str):
        self.__current_node = node_id

    def set_previous_node(self, prev_node_id: str):
        self.__previous_node = prev_node_id

    def get_current_position(self):
        return self.__current_position

    def get_current_node(self):
        return self.__current_node

    def get_previous_node(self):
        return self.__previous_node
