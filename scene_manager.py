# Imports
import pygame

# Initialize game engine
pygame.init()

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TITLE = "Name of Game"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)


class Scene():
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        print("title scene")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("down")
                if event.key == pygame.K_SPACE:
                    print("space")
                    self.next_scene = PlayScene()
    
    def update(self):
        pass
    
    def render(self):
        screen.fill(BLACK)
        text = FONT_LG.render(TITLE, 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.bottom = SCREEN_HEIGHT // 2
        screen.blit(text, rect)

    def terminate(self):
        self.next_scene = None


class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        print("play scene")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = EndScene()
    
    def update(self):
        pass
    
    def render(self):
        screen.fill(BLACK)
        text = FONT_LG.render("Playing", 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.bottom = SCREEN_HEIGHT // 2
        screen.blit(text, rect)

    def terminate(self):
        self.next_scene = None


class EndScene(Scene):
    def __init__(self):
        super().__init__()
        print("end scene")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("down")
                if event.key == pygame.K_SPACE:
                    print("space")
                    self.next_scene = TitleScene()
    
    def update(self):
        pass
    
    def render(self):
        screen.fill(BLACK)
        text = FONT_LG.render("Game Over", 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.bottom = SCREEN_HEIGHT // 2
        screen.blit(text, rect)

    def terminate(self):
        self.next_scene = None


class MyGame():
    def __init__(self, start_scene):
        self.active_scene = start_scene

    def is_quit_event(self, event, pressed_keys):
        x_out = event.type == pygame.QUIT
        ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        q = pressed_keys[pygame.K_q]

        return x_out or (ctrl and q)
        
    def run(self): 
        while self.active_scene != None:
            # event handling
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    self.active_scene.terminate()
                else:
                    filtered_events.append(event)

            # game logic
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()
            self.active_scene = self.active_scene.next_scene

            # update and tick
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    start_scene = TitleScene()
    
    game = MyGame(start_scene)
    game.run()
    pygame.quit()
