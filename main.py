import pygame, sys
from settings import *
from level import Level
class Game: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('True Game')
        self.clock = pygame.time.Clock()

        self.level = Level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(water_color)
            self.level.run()
            pygame.display.flip()
            self.clock.tick(fps)
if __name__ == '__main__':
    game = Game()
    game.run()