# Standard library imports

# Third-party imports
import pygame

# Local application imports
from .scene import Scene


class EndScene(Scene):
    """
    Represents the end or game over scene.

    Handles user input to restart the game and return to the title scene.
    """
    
    def __init__(self, game, **kwargs):
        """
        Initialize the special scene.

        Args:
            game (Game): The game object that this scene belongs to.
            **kwargs: Optional keyword arguments to configure scene behavior.
        """
        super().__init__(game, **kwargs)
        
    def load_assets(self):
        """
        Load the assets required for the scene.
        """
        self.font_xl = pygame.font.Font(None, 96)

    def cleanup(self):
        """
        Unload assets when the scene is no longer needed.
        """
        self.font_xl = None  # Unload font to free memory
        self.assets_loaded = False  # Force reload if re-entered

    def process_input(self, events, pressed_keys):
        """
        Handle user input for the title scene.

        Args:
            events (list): A list of pygame events that need to be processed.
            pressed_keys (set): A set of keys that are currently pressed.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.next_scene = self.game.scenes["title"]
                    self.terminated = True

    def update(self):
        """
        Update the state of the title scene.
        """
        pass

    def render(self):
        """
        Render the title screen onto the game window.
        """
        self.game.screen.fill(pygame.Color('black'))
        text = self.font_xl.render("End Scene", 1, pygame.Color('white'))
        rect = text.get_rect()
        rect.centerx = self.game.SCREEN_WIDTH // 2
        rect.centery = self.game.SCREEN_HEIGHT // 2
        self.game.screen.blit(text, rect)
