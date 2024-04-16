import math

import pygame

from src.aco_algorithm.aco import ACO
from src.utilities.graph import Graph
from src.utilities.node import Node
from src.visualisation.vis import Vis

graph = Graph()

import numpy as np
import pandas as pd

# generate an example synthetic dataset to be used for an input
np.random.seed(100)
# Number of content items
n_contents = 10

# Simulate some content items, creates a list of content item names
content_items = [f"Content_{i+1}" for i in range(n_contents)]

# Generate random similarity scores between content items (0 to 1)
# For simplicity, make the similarity matrix symmetric and set the diagonal to 0 (self-similarity ignored)
similarity_scores = np.random.rand(n_contents, n_contents)
similarity_scores = (similarity_scores + similarity_scores.T) / 2
np.fill_diagonal(similarity_scores, 0)

# Create a DataFrame for better readability
similarity_df = pd.DataFrame(similarity_scores, index=content_items, columns=content_items)

# Generate user preferences for content items
# For simplicity, assume we have one user with a preference score for each content item
user_preferences = np.random.rand(n_contents)

# Create a DataFrame for user preferences
user_preferences_df = pd.DataFrame(user_preferences, index=content_items, columns=["User_Preference"])

(similarity_df.round(2), user_preferences_df.round(2))

# Step 1 & 2: Create nodes and add them to the graph
for content_id in similarity_df.index:
    node = Node(content_id)
    graph.add_node(node)

# Step 3: Create edges based on content similarities
# We use a threshold to decide whether to create an edge or not
similarity_threshold = 0.5  # Example threshold

for i, content_id in enumerate(similarity_df.index):
    for j, related_content_id in enumerate(similarity_df.columns):
        # Check if similarity score exceeds the threshold and i != j to avoid self-loops
        if similarity_df.iloc[i, j] > similarity_threshold and i != j:
            # Here, you can choose to invert the similarity score to represent distance if needed
            distance = 1 / similarity_df.iloc[i, j]  # Example inversion
            graph.add_edge(content_id, related_content_id, distance)








# We can to converge on scores which are similar, balanced with exploration (should be a some content along the solution path which aren't that relevant, promoting new content)


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
                if path_length != 0:    # if ant has travelled (path variable length larger than 0)
                    current_node = ant.get_current_node()
                    previous_node = ant.get_previous_node()

                    new_pheromone_level = 1 / path_length

                    graph.update_pheromones(current_node, previous_node, new_pheromone_level)

                    graph.print_pheromone_levels()


        # Clear the screen
            visual.clear_screen()

        # Draw the graph
        visual.draw_graph(graph)
        visual.draw_ants(aco)

        # Update the display
        visual.update()

    pygame.quit()

if __name__ == '__main__':
    main()
