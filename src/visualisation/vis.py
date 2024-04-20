import math

import pygame
from src.graph_components.graph import Graph
from src.aco_algorithm.ant_manager import AntManager


class Visualiser:
    """
    Provides visualisation for the Ant Colony Optimisation (ACO) process using Pygame.
    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, window_size=(800, 600), window_title="ACO Visualiser"):
        """
        Initialises the ACO visualiser with a window size and title.

        :param window_size: A tuple representing the width and height of the window.
        :param window_title: The title of the window.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(window_title)
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

    def draw_graph(self, graph: Graph) -> None:
        """
        Draws the graph on the Pygame window.

        :param graph: The graph to be visualised.
        """
        self.screen.fill(self.BLACK)
        # Draw edges
        for edges, distance in graph.edges_dict.items():
            start_pos, end_pos = graph.nodes_dict[edges[0]].coordinates, graph.nodes_dict[edges[1]].coordinates
            pygame.draw.line(self.screen, self.WHITE, start_pos, end_pos, 1)
        # Draw nodes
        for node_id, node in graph.nodes_dict.items():
            pygame.draw.circle(self.screen, self.RED, node.coordinates, 20)
            text_surface = self.font.render(str(node_id), True, self.WHITE)
            text_pos = node.coordinates[0] - text_surface.get_width() // 2, node.coordinates[
                1] - text_surface.get_height() // 2
            self.screen.blit(text_surface, text_pos)
        pygame.display.flip()

    def draw_ants(self, AntManager) -> None:
        """
        Draws ants on the Pygame window based on their current positions in the ACO instance.

        :param aco: The ACO instance containing the ants to be visualised.
        """
        for ant in AntManager.ants:
            pygame.draw.circle(self.screen, self.GREEN, ant.get_current_position(), 5)

    def clear_screen(self) -> None:
        """
        Clears the Pygame window.
        """
        self.screen.fill(self.BLACK)

    def update(self) -> None:
        """
        Updates the Pygame display and controls the frame rate.
        """
        pygame.display.flip()
        self.clock.tick(60)

    @staticmethod
    def generate_node_coordinates(graph: Graph) -> None:
        """
        Generates and assigns coordinates to the nodes in the graph for visualisation purposes.

        :param graph: The graph whose nodes will be assigned coordinates.
        """
        center_of_screen = (400, 300)
        radius = 250    # Define the radius of the circle on which the nodes will be positioned

        # Calculate the number of nodes in the graph to determine the spacing between them
        num_nodes = len(graph.nodes_dict)

        # Calculate the increment angle based on the number of nodes to evenly distribute them in a circle
        angle_increment = 2 * math.pi / num_nodes
        for i, node_id in enumerate(graph.nodes_dict):
            # Calculate the angle for the current node to determine its position on the circle
            angle = i * angle_increment

            # Calculate the x and y coordinates of the node based on the center of the screen, radius, and angle
            # math.cos(angle) and math.sin(angle) determine the position on the circle based on the calculated angle
            x, y = center_of_screen[0] + radius * math.cos(angle), center_of_screen[1] + radius * math.sin(angle)

            # Update the node's position in the graph using the calculated coordinates
            graph.nodes_dict[node_id].set_coordinates(int(x), int(y))