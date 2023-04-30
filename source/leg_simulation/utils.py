# 座標を拡大する係数
scale_factor = 4000

# 座標を変換する関数（原点を画面中央に移動し、拡大）
def convert_coordinates(coord, width, height):
    x, y = coord
    x_transformed = int((x * scale_factor) + width // 2)
    y_transformed = int((-y * scale_factor) + height // 2)
    return x_transformed, y_transformed

# 座標からリンクのリストを作成する
def create_links(links, coordinates):
    link_coordinates = []
    for vertex1, vertex2 in links:
        if vertex1 in coordinates and vertex2 in coordinates:
            coord1 = coordinates[vertex1]
            coord2 = coordinates[vertex2]
            link_coordinates.append((coord1, coord2))
    return link_coordinates
