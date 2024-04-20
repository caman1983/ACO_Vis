import pygame

from src.aco_algorithm.ant_manager import AntManager
from src.aco_algorithm.eval_metrics import EvalMetrics
from src.graph_components.graph import Graph
from src.graph_components.node import Node
from src.utilities.similarity_df import SimilarityData
from src.visualisation.vis import Visualiser

# Setup code


# Create graph object
graph = Graph()

# Generate artificial similarity matrix
sim_data = SimilarityData(20)

# Populate graph with generated symmetric similarity matrix
# Add nodes
for content_id in sim_data.similarity_matrix.index:
    graph.add_node(Node(content_id))

# Add edges, based on similarity threshold
for i, content_id in enumerate(sim_data.similarity_matrix.index):
    for j, related_content_id in enumerate(sim_data.similarity_matrix.columns):
        if sim_data.similarity_matrix.iloc[i, j] > sim_data.similarity_threshold and i != j:
            similarity_score = sim_data.similarity_matrix.iloc[i, j]
            # Transform to distance (make items with large similarity values shorter paths)
            distance = 1 - similarity_score
            rounded_distance = round(distance, 2)
            graph.add_edge(content_id, related_content_id, rounded_distance)


def main():
    # Initialise node coordinates before creating ant objects
    Visualiser.generate_node_coordinates(graph)
    visualiser = Visualiser()

    ant_manager = AntManager(graph, 50, "Content_1")  # Initialise ACO  with the graph and number of ants

    # Flags to control the main simulation loop
    running = True
    iteration = 0

    # Main simulation loop
    while running and iteration < 5000:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Draw ants on first frame
            visualiser.draw_ants(ant_manager)
            # Process each ant's movement and state

        # Process each ant's movement and state
        for ant in ant_manager.ants:
            if ant.has_target_node():
                ant.move_toward_target()

            # If ant has reached target node
            elif not ant.has_target_node():
                # Generate path selection probabilities
                probabilities = ant.get_probabilities(70, 1)

                path_length = ant.get_path_length()
                next_node = ant.get_next_node(probabilities)
                ant.set_target_node(next_node)

                # Update pheromones if the ant has moved
                if path_length > 0:
                    current_node = ant.get_current_node()
                    previous_node = ant.get_previous_node()
                    new_pheromone_level = 1 / path_length
                    graph.update_pheromones(current_node, previous_node, new_pheromone_level)

                # Evaporate pheromones slightly after each iteration
                if ant.get_previous_node() is not None:  # combine with if path_length statment?
                    graph.evaporate(0.001)

                    # Increment iteration counter and log progress
                    iteration += 1
                    print(f"Iteration: {iteration}")

        # Clear the screen for the next frame
        visualiser.clear_screen()

        # Draw the current state of the graph and ants
        visualiser.draw_graph(graph)
        visualiser.draw_ants(ant_manager)

        # Update the display with the new frame
        visualiser.update()

        # After the main loop, extract and display the recommendations
    recommendations = EvalMetrics.extract_global_recommendations(graph)
    avg_similarity_score = EvalMetrics.average_similarity(recommendations, sim_data)
    diversity_score = EvalMetrics.calculate_diversity_score(recommendations, sim_data)
    coverage_score = EvalMetrics.calculate_coverage(len(graph.nodes_dict), recommendations)

    # Display final recommendations and statistics
    print("-" * 100)
    print(f"Recommendations: {recommendations}")
    print(f"Average Similarity Score: {avg_similarity_score}")
    print(f"Diversity Score: {diversity_score}")
    print(f"Coverage Score: {coverage_score}%")

    # Close pygame window
    pygame.quit()


if __name__ == '__main__':
    main()
