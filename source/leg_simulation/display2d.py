import pygame

class Display2D:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, transformed_coordinates, link_list):
        self.screen.fill((255, 255, 255))

        for link in link_list:
            start_pos = transformed_coordinates[link[0]]
            end_pos = transformed_coordinates[link[1]]

            pygame.draw.line(
                self.screen, (0, 0, 0), 
                (start_pos[0], start_pos[1]), 
                (end_pos[0], end_pos[1]), 3)

        pygame.display.flip()
        pygame.time.wait(10)

    def draw_2d(self, screen, font):
        positions = self.leg.get_positions()

        transformed_coordinates = {key: self.convert_coordinates(coord, self.screen_width, self.screen_height) for key, coord in positions.items()}

        links_coordinates = self.create_links_2D(self.link_list, transformed_coordinates)

        # ここから、pygameを使った2D表示を行います
        screen.fill((0, 0, 0))
        origin = np.array([self.screen_width // 2, self.screen_height // 2])

        # X=0, Y=0 の線を引く
        pygame.draw.line(screen, (128, 128, 128), (0, origin[1]), (self.screen_width, origin[1]), 3)
        pygame.draw.line(screen, (128, 128, 128), (origin[0], 0), (origin[0], self.screen_height), 3)

        # 座標軸の目盛りとラベルを描画
        marker_length = 0.02
        text_offset = 15
        scaled_step = int(self.convert_length(marker_length))

        for coord_val in range(0, self.screen_height//2, scaled_step):
            # X 軸
            pygame.draw.line(screen, (128, 128, 128), (0, origin[1] + coord_val), (self.screen_width, origin[1] + coord_val))
            pygame.draw.line(screen, (128, 128, 128), (0, origin[1] - coord_val), (self.screen_width, origin[1] - coord_val))

        for coord_val in range(0, self.screen_width//2, scaled_step):
            # Y 軸
            pygame.draw.line(screen, (128, 128, 128), (origin[0] + coord_val, 0), (origin[0] + coord_val, self.screen_height))
            pygame.draw.line(screen, (128, 128, 128), (origin[0] - coord_val, 0), (origin[0] - coord_val, self.screen_height))

        # 各頂点やリンクの描画は以下の部分で実装されています

        # 頂点を描画
        for vertex_name, coord in transformed_coordinates.items():

            pygame.draw.circle(screen, (255, 0, 0), coord, 5)
            
            if(vertex_name != 'A'):
                original_coord_mm = (positions[vertex_name][0] * 1000, positions[vertex_name][1] * 1000)
                label_text = f"{vertex_name} ({original_coord_mm[0]:.2f}, {original_coord_mm[1]:.2f})"
                label = font.render(label_text, True, (255, 255, 255))
                screen.blit(label, (coord[0] + 10, coord[1] - 10))

        # リンクを描画
        for link in links_coordinates:
            pygame.draw.line(screen, (0, 255, 0), link[0], link[1], 2)

        pygame.display.flip()


