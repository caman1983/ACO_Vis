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

node7 = Node("Node7")



# populate node dictionary
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)
graph.add_node(node4)

# adding it here makes sure it's in the middle
graph.add_node(node7)

graph.add_node(node5)
graph.add_node(node6)





graph.add_edge("Node1", "Node2", 5)
graph.add_edge("Node2", "Node3", 3)
graph.add_edge("Node3", "Node4", 50)


graph.add_edge("Node1", "Node6", 5)
graph.add_edge("Node6", "Node5", 1)
graph.add_edge("Node5", "Node7", 2)

# CONNECTS LINES
#graph.add_edge("Node4", "Node7", 50)




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

        for ant in aco.ants:
            if ant.has_target_node():  # if ant has a target node
                ant.move_toward_target()

            # if ant does not have a target node, set one todo: if target node has been reached this runs (check)
            elif not ant.has_target_node():
                # get probabilities based on probability decision rule
                probabilities = ant.get_probabilities()
                # get next node based on probabilities
                next_node = ant.get_next_node(probabilities)
                # set target
                ant.set_target_node(next_node)



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
