# Standard library imports

# Third-party imports
import pygame

# Local application imports
from scenes.title_scene import TitleScene
from scenes.play_scene1 import PlayScene1
from scenes.play_scene2 import PlayScene2
from scenes.special_scene import SpecialScene
from scenes.end_scene import EndScene


class Game():

    def __init__(self):
        # Screen configuration constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.TITLE = "Name of Game"
        self.FPS = 60

        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.TITLE)

        self.scenes = {
            "title": TitleScene(self, delay_asset_loading=False),
            "play1": PlayScene1(self, cleanup_on_terminate=True),
            "play2": PlayScene2(self, cleanup_on_terminate=True),
            "special": SpecialScene(self, delay_asset_loading=False, cleanup_on_terminate=False),
            "end": EndScene(self)
        }

        self.active_scene = self.scenes["title"]
        self.active_scene.enter()

    def is_quit_event(self, event, pressed_keys):
        x_out = event.type == pygame.QUIT
        ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        q = pressed_keys[pygame.K_q]

        return x_out or (ctrl and q)
        
    def run(self):
        running = True

        while running:
            # Get user input
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    running = False
                else:
                    filtered_events.append(event)

            # Manage scene
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()

            # Check for scene change
            current_scene = self.active_scene
            self.active_scene = self.active_scene.next_scene

            if current_scene is not self.active_scene:
                self.previous_scene = current_scene
                current_scene.exit()  # Scene exit logic runs first

                if current_scene.terminated:  # If flagged, cleanup happens now
                    current_scene.cleanup()

                self.active_scene.enter()
                
            # Update and tick
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
