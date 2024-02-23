import math

import pygame
import sys

from src.aco import ACO
from src.ant import Ant
from src.graph import Graph
from src.node import Node

# Initialises pygame library
pygame.init()

# Variables for display parameters
window_size = (800, 600)
window_title = "ACO Visualizer"

# Create pygame window using display variables
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_title)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()
##############################

graph = Graph()

node1 = Node("Node1")
node2 = Node("Node2")
node3 = Node("Node3")
node4 = Node("Node4")
node5 = Node("Node5")


# populate node dictionary
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)
graph.add_node(node4)
graph.add_node(node5)

# graph.print_node_dict()


graph.add_edge("Node1", "Node2", 10)
graph.add_edge("Node1", "Node3", 20)
graph.add_edge("Node4", "Node1", 30)
graph.add_edge("Node5", "Node2", 30)

#ant1 = Ant(graph, "Node1")

#ant1.select_next_node()


def draw_graph():
    screen.fill(BLACK)
    # iterate through every item in edges dictionary
    # edge = key (containing tuple of connected nodes as strings)
    # distance = pair-values (edge weight between nodes)
    # draw a line between two nodes coordinates
    for edge, distance in graph.edges_dict.items():
        # edge = current iteration of tuple of edges
        start_pos = graph.nodes_dict[edge[0]].coordinates
        # access node dictionary using second element in edges tuple as id, get that nodes coordinates
        end_pos = graph.nodes_dict[edge[1]].coordinates
        pygame.draw.line(screen, WHITE, start_pos, end_pos, 1)  # Draw line for edge

    # draw a circle at nodes coordinates
    for node_id, node in graph.nodes_dict.items():
        pygame.draw.circle(screen, RED, node.coordinates, 5)  # Draw node as a circle

    pygame.display.flip()

# draw ants by iterating through ants object list in ACO class
def draw_ants(aco):
    # iterate through ants object list
    for ant in aco.ants:
        # get string_id of ants current node
        # get ants current position by using their "current node" string ID to retrieve the node object from the node dictionary
        node_id = ant.current_node
        current_position = ant.current_position
        pygame.draw.circle(screen, GREEN, current_position, 5)


# todo: NOT MY CODE, REVIEW
def generate_node_coordinates():
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


def main():
    # needs to be first otherwise ants will be created before nodes have their coordinates
    generate_node_coordinates()

    aco = ACO(graph, 3)



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_ants(aco)
        for ant in aco.ants:
            if ant.target_node_id is not None:  # if ant has a target node
                ant.move_toward_target()

            # if ant does not have a target node, set one
            else:
                next_target_id = ant.select_next_node()
                ant.set_target_node(next_target_id)

        # Clear the screen
        screen.fill(BLACK)

        # Draw the graph
        draw_graph()
        draw_ants(aco)


        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()

