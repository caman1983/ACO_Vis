import math

import pygame

from src.aco_algorithm.aco import ACO
from src.utilities.graph import Graph
from src.utilities.node import Node
from src.utilities.similarity_df import Similarity_DF
from src.visualisation.vis import Vis

# Create graph object
graph = Graph()

# Generate synthetic data
sim_data = Similarity_DF(20)

# Populate graph with generated symmetric similarity matrix
# Add nodes
for content_id in sim_data.similarity_df.index:
    graph.add_node(Node(content_id))

# Add edges, based on similarity threshold (optional)
for i, content_id in enumerate(sim_data.similarity_df.index):
    for j, related_content_id in enumerate(sim_data.similarity_df.columns):
        if sim_data.similarity_df.iloc[i, j] > sim_data.similarity_threshold and i != j:
            similarity_score = sim_data.similarity_df.iloc[i, j]
            # Transform to distance (make items with large similarity values shorter paths)
            distance = 1 - similarity_score
            rounded_distance = round(distance, 2)
            graph.add_edge(content_id, related_content_id, rounded_distance)



def main():
    # needs to be first otherwise ants will be created before nodes have their coordinates
    Vis.generate_node_coordinates(graph)
    visual = Vis()

    aco = ACO(graph, 50)
    iteration = 0

    # setup code for pygame loop
    while iteration < 2000:
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
                probabilities = ant.get_probabilities(70,1)

                # must be here as calling get_next_node removes current node from path if nowhere to go
                path_length = ant.get_path_length()

                # get next node based on probabilities
                next_node = ant.get_next_node(probabilities)
                # set target
                ant.set_target_node(next_node)

                # ---------------- TESTING PHEROMONE DEPOSITING


                # if the ant has travelled to a new node, update pheromones on the edge
                if path_length != 0:    # if ant has travelled (path variable length larger than 0)
                    current_node = ant.get_current_node()
                    previous_node = ant.get_previous_node()

                    new_pheromone_level = 1 / path_length

                    graph.update_pheromones(current_node, previous_node, new_pheromone_level)

                    #graph.print_pheromone_levels()
                    # satisfied when ant reaches its target and previous node is not none (ant has not just spawned)


                if ant.get_previous_node() is not None:
                    graph.evaporate(0.001)

                iteration += 1
                print("Iteration:",iteration)

        # Clear the screen
        visual.clear_screen()

        #FINISHED!!!

        # Draw the graph
        visual.draw_graph(graph)
        visual.draw_ants(aco)

        # Update the display
        visual.update()

    recommendations = aco.extract_global_recommendations()
    avg_sim_score = aco.average_similarity(recommendations, sim_data)
    div_score = aco.calculate_diversity_score(recommendations, sim_data)
    coverage = aco.calculate_coverage(len(graph.nodes_dict), recommendations)

    print("-" * 100)
    print("Recommendations: ", recommendations)

    print("Average Similarity Score:", avg_sim_score)
    print("Diversity Score: ", div_score)
    print("Coverage Score:", coverage, "%")

    graph.print_pheromone_levels()

    pygame.quit()

if __name__ == '__main__':
    main()
