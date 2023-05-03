import pygame
from pygame.locals import *

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from draw_functions import draw_2d_objects, draw_graph

class PygameManager:
    def __init__(self):
        self.time_data = [0, 1, 2, 3, 4, 5]
        self.speed_data = [0, 2, 4, 6, 8, 10]
        self.line_color = (255, 255, 255)
        self.origin = (50, 450)
        self.axis_scale = (100, 50)

    def draw_pygame_window(self):
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

            # グラフ表示
            draw_graph(screen, self.speed_data, self.line_color, self.origin, self.axis_scale)

            pygame.display.flip()

        pygame.quit()