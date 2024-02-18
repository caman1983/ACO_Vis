import pygame
import sys

import ant
from src.graph import Graph
from src.node import Node


def foo():
    # Initialises pygame library
    pygame.init()

    # Variables for display parameters
    window_size = (800, 600)
    window_title = "ACO Visualizer"

    # Create pygame window using display variables
    pygame.display.set_mode(window_size)
    pygame.display.set_caption(window_title)

    # Begin game loop using a flag to control
    running = True
    while running:
        # pygame.event.get():   returns a list of events (mouse clicks, keyboard presses etc.)
        # iterates through each event in events list & sets control flag to false if user attempts to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game window at the end of each iteration
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def main():
    graph = Graph()

    node1 = Node("Node1")
    node2 = Node("Node2")
    node3 = Node("Node3")

    # populate node dictionary
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    graph.print_node_dict()

    graph.add_edge("Node1", "Node2", 10)
    graph.add_edge("Node1", "Node3", 14)

    connected_edges = graph.get_connected_nodes("Node1")
    print(connected_edges)

    ant1 = ant.Ant(graph, "Node1")
    probability = ant1.select_next_node()
    print(probability)
    # IT FUCKING WORKS


if __name__ == '__main__':
    main()
