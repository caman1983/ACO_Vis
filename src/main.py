import math

import pygame

from src.aco_algorithm.aco import ACO
from src.utilities.graph import Graph
from src.utilities.node import Node
from src.visualisation.vis import Vis

graph = Graph()

node1 = Node("Node1")
node2 = Node("Node2")
node3 = Node("Node3")
node4 = Node("Node4")
node5 = Node("Node5")
node6 = Node("Node6")

# populate node dictionary
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)
graph.add_node(node4)
# todo: Last node to be generated causes ant to get stuck
graph.add_node(node5)
graph.add_node(node6)

graph.add_edge("Node1", "Node2", 50)
graph.add_edge("Node2", "Node3", 20)
graph.add_edge("Node2", "Node5", 10)
graph.add_edge("Node4", "Node2", 300)
graph.add_edge("Node6", "Node2", 2)

#ant.get_next_node(get_probabilities())

#or

#ant.get_next_node().probabilities() ?????


def main():
    # needs to be first otherwise ants will be created before nodes have their coordinates
    Vis.generate_node_coordinates(graph)
    visual = Vis()

    aco = ACO(graph, 1)

    # setup code for pygame loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # draw ants on every game loop interation
        visual.draw_ants(aco)

        # iterate through ant objects
        for ant in aco.ants:
            if ant.has_target_node():  # if ant has a target node
                ant.move_toward_target()

            # if ant does not have a target node, set one
            else:
                ant.set_target_node(ant.get_next_node(ant.get_probabilities()))


        # Clear the screen
        visual.clear_screen()

        # Draw the graph
        visual.draw_graph(graph)
        visual.draw_ants(aco)

        # Update the display
        visual.update()

    pygame.quit()


# todo: set a target node for the ant, update pheromones

if __name__ == '__main__':
    main()
