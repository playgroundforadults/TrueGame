import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Initializes the Pygame library modules to allow usage of its features.
        pygame.init()
        
        # Creates the main display window with the width and height specified in the settings file.
        self.screen = pygame.display.set_mode((width, height))
        
        # Sets the title of the window to 'True Game'.
        pygame.display.set_caption('True Game')
        
        # Creates a clock object to track time and control the game's framerate.
        self.clock = pygame.time.Clock()

        # Instantiates the Level class, which handles the map, player, and enemies.
        self.level = Level()

    def run(self):
        # Starts the main game loop which runs indefinitely until the user quits.
        while True:
            # Iterates through all events (like key presses, mouse clicks) in the event queue.
            for event in pygame.event.get():
                # Checks if the user clicked the close button on the window.
                if event.type == pygame.QUIT:
                    # Uninitializes Pygame modules and closes the window.
                    pygame.quit()
                    # Terminates the Python script.
                    sys.exit()

            # Fills the entire screen with black to clear the previous frame's drawings.
            self.screen.fill('black')
            
            # Calls the run method of the level object to update and draw the game state.
            self.level.run()
            
            # Checks if the player's health is 0 or less.
            if self.level.player.health <= 0:
                # Re-instantiates the Level class, creating a fresh game state.
                self.level = Level()
            # -----------------------------
            
            # Updates the full display surface to the screen (double buffering).
            pygame.display.flip()
            
            # Pauses the loop to ensure the game runs at the specified frames per second (FPS).
            self.clock.tick(fps)

if __name__ == '__main__':
    # Creates an instance of the Game class.
    game = Game()
    # Starts the game loop.
    game.run()