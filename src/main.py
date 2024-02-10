import pygame
import sys


def main():
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


if __name__ == '__main__':
    main()
