import math

import pygame

from src.aco_algorithm.aco import ACO
from src.utilities.graph import Graph


# class for controlling visual element of aco
class Vis:
    def __init__(self):
        # Initialises pygame library
        pygame.init()

        # For display parameters
        window_size = (800, 600)
        window_title = "ACO Visualizer"

        # Create pygame window using display variables
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(window_title)

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.font = pygame.font.Font(None, 24)  # Default font, size 24


        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()




    # draw graph
    def draw_graph(self, graph: Graph):
        self.screen.fill(self.BLACK)
        for edges, distance in graph.edges_dict.items():
            start_pos = graph.nodes_dict[edges[0]].coordinates
            end_pos = graph.nodes_dict[edges[1]].coordinates
            pygame.draw.line(self.screen, self.WHITE, start_pos, end_pos, 1)

        for node_id, node in graph.nodes_dict.items():
            pygame.draw.circle(self.screen, self.RED, node.coordinates, 20)  # Increased node size for visibility

            # Render the node ID text
            text_surface = self.font.render(str(node_id), True, self.WHITE)
            # Calculate text position (centered on the node circle)
            text_pos = (node.coordinates[0] - text_surface.get_width() / 2,
                        node.coordinates[1] - text_surface.get_height() / 2)
            self.screen.blit(text_surface, text_pos)

        pygame.display.flip()

    # draw ants by iterating through ants object list in ACO class
    def draw_ants(self, aco: ACO):
        # iterate through ants object list
        for ant in aco.ants:
            # draws ants based on their current coordinates
            pygame.draw.circle(self.screen, self.GREEN, ant.get_current_position(), 5)

    def clear_screen(self):
        self.screen.fill(self.BLACK)

    def update(self):
        # Update the display
        pygame.display.flip()
        self.clock.tick(60)

    # todo: method is static as it does not change the class or instance state, it can be called without
        # instantiating the class
    # todo: NOT MY CODE, REVIEW
    @staticmethod
    def generate_node_coordinates(graph: Graph):
        center_of_screen = (400, 300)
        radius = 250
        num_nodes = len(graph.nodes_dict)
        angle_increment = 2 * math.pi / num_nodes
        for i, node_id in enumerate(graph.nodes_dict):
            angle = i * angle_increment
            x = center_of_screen[0] + radius * math.cos(angle)
            y = center_of_screen[1] + radius * math.sin(angle)
            # Update the node's coordinates directly or use the set_coordinates method
            graph.nodes_dict[node_id].set_coordinates(int(x), int(y))

