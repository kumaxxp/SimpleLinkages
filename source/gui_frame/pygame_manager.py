import pygame
from pygame.locals import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from draw_functions import draw_2d_objects

class PygameManager:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.time_data = [0, 1, 2, 3, 4, 5]
        self.speed_data = [0, 2, 4, 6, 8, 10]
        self.line_color = (255, 255, 255)
        self.origin = (50, 450)
        self.axis_scale = (100, 50)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D View")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            screen.fill((0, 0, 0))

            # 2D オブジェクトの描画
            draw_2d_objects(screen)

            pygame.display.flip()

        pygame.quit()