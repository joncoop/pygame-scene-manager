# Standard library imports

# Third-party imports
import pygame

# Local application imports


class Scene():
    """
    A base class for defining and managing a scene in a game.

    This class provides the structure for scene management, including loading assets, handling scene transitions, and freeing 
    resources when the scene is no longer needed. It can be extended to implement specific scenes (e.g., menu, gameplay, game over).

    Attributes:
        game (Game): The game object that the scene belongs to. It provides access to the game-wide resources like the screen, event loop, etc.
        cleanup_on_terminate (bool): Flag indicating whether to clean up resources when the scene is terminated. Default is True.
        delay_asset_loading (bool): Flag indicating whether to delay asset loading until the scene is entered. Default is True.
        assets_loaded (bool): Flag indicating whether the scene's assets have been loaded.

    Methods:
        __init__(game, **kwargs): Initializes a new scene with the provided game object and optional configuration.
        load_assets(): Loads the assets required for the scene (override this method in subclasses).
        enter(): Defines actions when the scene is entered (override this method in subclasses).
        exit(): Defines actions when the scene is exited (override this method in subclasses).
        terminate(): Defines actions when the scene is completed or terminated (override this method in subclasses).
        cleanup(): Frees resources and cleans up when the scene is terminated (override this method in subclasses).
        process_input(events, pressed_keys): Processes user input for the scene (abstract method to be implemented in subclasses).
        update(): Updates the scene's state (abstract method to be implemented in subclasses).
        render(): Renders the scene onto the screen (abstract method to be implemented in subclasses).
    """
    def __init__(self, game, **kwargs):
        """
        Initialize a new scene with the provided game object and optional configuration.

        Args:
            game (Game): The game object that this scene belongs to. It provides access to game-wide resources like the screen, event loop, etc.
            **kwargs: Optional keyword arguments to customize the scene's behavior:
                - 'cleanup_on_terminate' (bool): Whether to clean up resources when the scene is terminated. Default is True.
                - 'delay_asset_loading' (bool): Whether to delay asset loading until the scene is entered. Default is True.

        Example:
            def __init__(self, game, **kwargs):
                super().__init__(game, **kwargs)
                # custom initialization logic for the scene, if needed

        This method is used to initialize the scene, including setting up the necessary configurations such as whether to delay asset loading 
        or whether cleanup should occur when the scene terminates.
        """
        self.game = game
        self.cleanup_on_terminate = kwargs.get('cleanup_on_terminate', True)
        self.delay_asset_loading = kwargs.get('delay_asset_loading', True)
        self.assets_loaded = False
        self.terminated = False

        if not self.delay_asset_loading:
            self.load_assets()

    def load_assets(self):
        """
        Override this method to load any assets required for the scene, such as images, sounds, or fonts.

        Example:
            In a gameplay scene, you might want to load images and sounds specific to that scene when it's entered.

            def load_assets(self):
                super().load_assets()
                self.background_image = pygame.image.load("background.png")
                self.sound_effect = pygame.mixer.Sound("jump.wav")

        This method is called when the scene is entered and assets need to be loaded. If the scene has specific assets 
        (like images or sounds), they should be loaded here.
        """
        pass

    def enter(self):
        """
        Override this method to define actions that should occur when the scene is entered.

        Example:
            In a menu scene, you might want to start background music or initialize specific elements when the scene 
            is displayed.

            def enter(self):
                super().enter()
                pygame.mixer.music.play(-1)  # Start background music when entering the scene

        This method is called when the scene is first activated or when it's revisited after being exited.
        """
        self.next_scene = self

        if not self.assets_loaded:
            self.load_assets()
            self.assets_loaded = True

    def exit(self):
        """
        Override this method to define actions that should occur when the scene is exited.

        Example:
            In a game scene, you might want to pause or stop background music when the player leaves the scene.

            def exit(self):
                super().exit()
                pygame.mixer.music.pause()  # Pause music when exiting the scene

        This method is called when the scene when transitioning to another scene. This method preserves the overall
        state of the scene so it can be returned to.
        """
        pass

    def terminate(self):
        """
        Override this method to define actions that should occur when the scene is complete or is being terminated.

        Example:
            In a menu scene, you might want to perform some final actions before fully exiting, like saving game 
            progress or stopping background music.

            def terminate(self):
                super().terminate()
                self.game.save_progress()  # Save game progress before terminating the scene
                pygame.mixer.music.stop()  # Stop music before the scene is terminated

        This method is called when the scene is complete, typically when the player is leaving the scene or transitioning
        to another scene. It's a good place to perform any necessary final cleanup, saving, or stopping background processes 
        that should only occur once the scene is no longer active.
        """
        if self.cleanup_on_terminate:
            self.cleanup()

    def cleanup(self):
        """
        Override this method to free up resources that are no longer needed when the scene is terminated.

        Example:
            In a gameplay scene, you might want to unload textures, sounds, or other assets to free up memory when the 
            scene ends.

            def cleanup(self):
                super().cleanup()
                self.background_image = None  # Unload background image to free memory
                self.sound_effect = None  # Unload sound effect to free memory

        This method is called when the scene is being terminated or when transitioning to another scene. It's a good place 
        to free up memory or other resources that were loaded for the scene. Resources like images, sounds, or large data 
        structures should be unloaded to ensure that they do not consume memory unnecessarily.
        """
        pass

    def process_input(self, events, pressed_keys):
        """Process the user input for this scene (e.g., keyboard, mouse)."""
        raise NotImplementedError

    def update(self):
        """Update the state of this scene, e.g., moving objects, game logic."""
        raise NotImplementedError

    def render(self):
        """Render the scene onto the screen, e.g., drawing sprites, backgrounds."""
        raise NotImplementedError
    