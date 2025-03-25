import os
import cv2
import numpy as np
import math
import pandas as pd

# ディレクトリのパスを指定
directory_path = 'preparation_before'

# 座標が格納されている配列から始点と終点を取り出す
# Retrieve the starting and ending points from the array where the coordinates are stored
def filter_coords(coords):
    start_coords = coords[0]
    end_coords = coords[-1]
    if len(coords) > 2:
        for i in range(1, len(coords)):
            if start_coords[1] > coords[i][1]:  
                start_coords = coords[i]
            if end_coords[1] < coords[i][0]:  
                end_coords = coords[i]
        return [start_coords, end_coords]
    else:
        return coords
# 指定の直線に対して、指定の座標から直角になるように線を引く
# Draw a line at a right angle from the specified coordinates to the specified line
def right_angle_line(line_coords, point_coords, color):
    x1, y1 = line_coords[0]
    x2, y2 = line_coords[1]

    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    orthogonal_angle = angle - 90

    if point_coords.ndim == 1:
        point_coords = point_coords[np.newaxis, :]
    
    x_start = point_coords[0, 0] + int(1000 * math.cos(math.radians(orthogonal_angle)))
    y_start = point_coords[0, 1] + int(1000 * math.sin(math.radians(orthogonal_angle)))
    x_end = point_coords[0, 0] - int(1000 * math.cos(math.radians(orthogonal_angle)))
    y_end = point_coords[0, 1] - int(1000 * math.sin(math.radians(orthogonal_angle)))
    startpoint = (x_start, y_start)
    endpoint = (x_end, y_end)
    cv2.line(image, tuple(point_coords[0]), startpoint, color, 1)
    cv2.line(image, tuple(point_coords[0]), endpoint, color, 1)

    
# tifファイルの読み込みとファイル名の一覧表示
tif_files = [f for f in os.listdir(directory_path) if f.endswith('.tif')]
for file in tif_files:
    file_path = os.path.join(directory_path, file)
    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)  # 画像を読み込む（IMREAD_UNCHANGEDを使用すると、元のフォーマットで画像が読み込まれます）
    print(f'Loaded {file}')
    filename_without_ext = os.path.splitext(file)[0]
    
    red = [0,0,255]
    green = [0,255,0]
    magenta = [255,0,255]
    blue = [255,0,0]
    
    red_coords = np.argwhere(np.all(image == red, axis=-1))[:, [1, 0]]
    green_coords = np.argwhere(np.all(image == green, axis=-1))[:, [1, 0]]
    magenta_coords = np.argwhere(np.all(image == magenta, axis=-1))[:, [1, 0]]
    blue_coords = np.array(filter_coords(np.argwhere(np.all(image == blue, axis=-1))))[:, [1, 0]]

    # 指定の直線を体長(横)，指定の座標を胸鰭(上,下)の先端とし，関数right_angle_lineを呼び出す
    # Call the function right_angle_line with the specified line as the body length (horizontal) and the specified coordinate as the tip of the pectoral fin (upper,lower)
    right_angle_line(blue_coords,red_coords,(0,0,255))
    right_angle_line(blue_coords,green_coords,(0,255,0))
    right_angle_line(blue_coords,magenta_coords,(255,0,255))
    cv2.line(image, red_coords[0], red_coords[0], (255, 255, 0), 1)
    cv2.line(image, green_coords[0], green_coords[0], (255, 255, 0), 1)
    cv2.line(image, magenta_coords[0], magenta_coords[0], (0, 254, 254), 1)

    # ファイル名を動的に生成
    filename_without_ext = os.path.splitext(file)[0]
    new_file_path = f'preparation_after/{filename_without_ext}.tif'
    
    # 画像を保存
    cv2.imwrite(new_file_path, image)
    print(f'Saved {new_file_path}')
