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
graph.add_node(node5)
graph.add_node(node6)


graph.add_edge("Node1", "Node2", 10)
graph.add_edge("Node2", "Node3", 10)
graph.add_edge("Node3", "Node4", 10)
graph.add_edge("Node4", "Node5", 10)
graph.add_edge("Node5", "Node6", 14)
graph.add_edge("Node2", "Node4", 12)
graph.add_edge("Node1", "Node6", 15)

graph.add_edge("Node4", "Node2", 15)
graph.add_edge("Node3", "Node4", 15)
graph.add_edge("Node2", "Node5", 15)
graph.add_edge("Node1", "Node6", 15)





def main():
    # needs to be first otherwise ants will be created before nodes have their coordinates
    Vis.generate_node_coordinates(graph)
    visual = Vis()

    aco = ACO(graph, 20)

    # setup code for pygame loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # draw ants on every game loop interation
        visual.draw_ants(aco)

        for ant in aco.ants:
            if ant.has_target_node():  # if ant has a target node, runs until target node is reached
                ant.move_toward_target()

            # if ant does not have a target node, set one - only runs when ant has reached target OR when the program starts
            # when ant has reached its target, set a new one
            elif not ant.has_target_node():
                # get probabilities based on probability decision rule
                probabilities = ant.get_probabilities()

                # must be here as calling get_next_node removes current node from path if nowhere to go
                path_length = ant.get_path_length()

                # get next node based on probabilities
                next_node = ant.get_next_node(probabilities)
                # set target
                ant.set_target_node(next_node)

                # ---------------- TESTING PHEROMONE DEPOSITING
                # satisfied when ant reaches its target and previous node is not none (ant has not just spawned)
                if ant.get_previous_node() is not None:
                    graph.evaporate(0.05)


                # if the ant has travelled to a new node, update pheromones on the edge
                if path_length != 0:    # if ant has travelled (path length larger than 0)
                    current_node = ant.get_current_node()
                    previous_node = ant.get_previous_node()

                    new_pheromone_level = 1 / path_length

                    graph.update_pheromones(current_node, previous_node, new_pheromone_level)

                    graph.print_pheromone_levels()

                    #current_pheromone = graph.get_pheromone_level((current_node, next_node))





        ## demo


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
