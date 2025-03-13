# Standard library imports

# Third-party imports
import pygame

# Local application imports
from game import Game


def main():
    pygame.init()

    game = Game()
    game.run()

    
# Let's do this!
if __name__ == "__main__":
    main()
