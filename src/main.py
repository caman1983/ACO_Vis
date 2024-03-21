import math

import pygame

from src.aco_algorithm.aco import ACO
from src.utilities.graph import Graph
from src.utilities.node import Node
from src.visualisation.vis import Vis

graph = Graph()

node1 = Node("Comedy")
node2 = Node("Drama")
node3 = Node("Sci-Fi")
node4 = Node("Romance")
node5 = Node("Action")
node6 = Node("Western")
node7 = Node("Crime")
node8 = Node("Horror")
node9 = Node("War")
node10 = Node("Adventure")

node11 = Node("Art")
node12 = Node("Martial arts")
node13 = Node("Heist")
node14 = Node("Historical")
node15 = Node("Superhero")
node16 = Node("Spy")
node17 = Node("Fantasy")
node18 = Node("Mystery")
node19 = Node("Family")
node20 = Node("Musical")


# populate node dictionary
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)
graph.add_node(node4)
graph.add_node(node5)
graph.add_node(node6)
graph.add_node(node7)
graph.add_node(node8)
graph.add_node(node9)
graph.add_node(node10)

graph.add_edge("Comedy", "Drama", 12)
graph.add_edge("Western", "Action", 18)
graph.add_edge("War", "Action", 5)
graph.add_edge("Adventure", "Action", 11)
graph.add_edge("Adventure", "Sci-Fi", 19)
graph.add_edge("Crime", "Action", 7)
graph.add_edge("Crime", "Drama", 6)
graph.add_edge("Action", "Drama", 22)
graph.add_edge("Horror", "Drama", 14)
graph.add_edge("Romance", "Drama", 17)
graph.add_edge("Romance", "Adventure", 17)
graph.add_edge("Horror", "Drama", 17)










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


                # should this be indented?
                if path_length != 0:    # if ant has travelled (path length larger than 0)
                    current_node = ant.get_current_node()

                    new_pheromone_level = 1 / path_length

                    graph.update_pheromones(current_node, next_node, new_pheromone_level)

                    #graph.print_pheromone_levels()

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
